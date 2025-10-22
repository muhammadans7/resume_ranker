from django.urls import path
from .views import JobUploadAPIView

urlpatterns = [
    path('jobs/', JobUploadAPIView.as_view(), name='job-upload'),
]