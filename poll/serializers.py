from rest_framework import serializers
from .models import PollQuestion, PollChoice, PLike


class PLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PLike
        fields = "__all__"


class PollChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollChoice
        fields = ["choice_text", "votes", "answer"]


class PollQuestionSerializer(serializers.ModelSerializer):
    choice = PollChoiceSerializer(many=True, read_only=True)
    p_likes = PLikeSerializer(many=True, read_only=True)

    class Meta:
        model = PollQuestion
        fields = "__all__"
