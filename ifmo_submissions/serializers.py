from rest_framework import serializers

from submissions.models import ScoreAnnotation
from submissions.serializers import ScoreSerializer


class ScoreAnnotationSerializer(serializers.ModelSerializer):

    score = ScoreSerializer()

    class Meta:
        model = ScoreAnnotation
        fields = (
            'score',
            'annotation_type',
            'creator',
            'reason',
        )

