from django.urls import path
from .views import CandidateMatchingAPIView

urlpatterns = [
    path('match_candidates/' , CandidateMatchingAPIView.as_view() , name="match-candidates")
]