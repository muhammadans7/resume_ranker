from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CandidateSerializer
from .models import Candidate
from .services.extract_text import extract_text
from .services.openai_service import get_embedding
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CandidateUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload a candidate resume and extract text + embedding",
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_FORM,
                description="Candidate name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'email',
                openapi.IN_FORM,
                description="Candidate email",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'resume',
                openapi.IN_FORM,
                description="Candidate resume file (PDF or DOCX)",
                type=openapi.TYPE_FILE
            ),
        ],
        responses={201: "Candidate created successfully"},
    )

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        candidate = serializer.save()

        file_path = candidate.resume.path
        ext =  os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            text = extract_text(file_path=file_path, file_type="pdf")
        elif ext == '.docx':
            text = extract_text(file_path=file_path, file_type='docx')

        else:
            text = ""
        
        candidate.extracted_text = text 

        if text:
            embedding = get_embedding(text)
            candidate.embedding = embedding

        candidate.save()
        return Response(CandidateSerializer(candidate).data , status=status.HTTP_201_CREATED)
    
