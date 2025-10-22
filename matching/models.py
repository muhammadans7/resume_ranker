from django.db import models
from jobs.models import Job
from candidates.models import Candidate
from django.contrib.postgres.fields import ArrayField

class MatchResult(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    match_score = models.FloatField()
    missing_skills = ArrayField(
        models.CharField(max_length=200) , blank=True, default=list
    )
    analysis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

