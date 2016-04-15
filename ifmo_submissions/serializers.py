from rest_framework import serializers

from submissions.models import ScoreAnnotation


class ScoreAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScoreAnnotation
        fields = (
            'score',
            'annotation_type',
            'creator',
            'reason',
        )

