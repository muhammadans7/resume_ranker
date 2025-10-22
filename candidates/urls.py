from django.urls import path
from .views import CandidateUploadAPIView

urlpatterns = [
    path('candidates/', CandidateUploadAPIView.as_view(), name='candidate-upload'),
]
