from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from candidates.models import Candidate
from jobs.models import Job
from matching.services.matching_service import cosine_similarity
from matching.services.explanation_service import generate_match_explanation
from .serializers import JobMatchRequestSerializer , CandidateMatchResultSerializer

class CandidateMatchingAPIView(APIView):

    @swagger_auto_schema(
        request_body=JobMatchRequestSerializer,
        responses={200: CandidateMatchResultSerializer(many=True)}
    )

    def post(self, request):
        serializer = JobMatchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_id = serializer.validated_data["job_id"]

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error" : "Job not found"} , status=status.HTTP_404_NOT_FOUND)
        
        if not job.embedding:
            return Response({"error" : "Job has no embedding"} , status=status.HTTP_400_BAD_REQUEST)
        
        candidates = Candidate.objects.exclude(embedding__isnull=True)
        results = []

        for candidate in candidates:
            similarity = cosine_similarity(job.embedding, candidate.embedding)
            explanation = generate_match_explanation(
                job.description, candidate.extracted_text, similarity
            )

            results.append({
                "candidate" : candidate.name,
                "email" : candidate.email,
                "similarity" : round(similarity, 4),
                "explanation" : explanation
            })

        results.sort(key=lambda x : x["similarity"] , reverse=True)
        return Response(results, status=status.HTTP_200_OK)



