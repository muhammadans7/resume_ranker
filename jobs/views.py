from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from .serializers import JobSerializer
from candidates.services.openai_service import get_embedding

class JobUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Create a job posting and generate an embedding from its description",
        manual_parameters=[
            openapi.Parameter(
                'title',
                openapi.IN_FORM,
                description="Job title",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'description',
                openapi.IN_FORM,
                description="Job description text",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={201: "Job created successfully"},
    )
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = serializer.save()

        text = job.description
        embedding = get_embedding(text)
        job.embedding = embedding
        job.save()

        return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
