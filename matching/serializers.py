from rest_framework import serializers


class JobMatchRequestSerializer(serializers.Serializer):
    job_id = serializers.IntegerField(required=True, help_text="ID of the job to match candidates for")

class CandidateMatchResultSerializer(serializers.Serializer):
    candidate = serializers.CharField()
    email = serializers.EmailField()
    similarity = serializers.FloatField()