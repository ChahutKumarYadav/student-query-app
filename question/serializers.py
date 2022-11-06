from rest_framework import serializers
from .models import Question, QLike, ALike, CommentLike, Comment, Answer


class ALikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALike
        fields = "__all__"


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    c_likes = CommentLikeSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    a_likes = ALikeSerializer(read_only=True, many=True)
    comments = CommentLikeSerializer(read_only=True, many=True)

    class Meta:
        model = Answer
        fields = "__all__"


class QLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QLike
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    q_likes = QLikeSerializer(read_only=True, many=True)
    answered_question = AnswerSerializer(read_only=True, many=True)
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')


    class Meta:
        model = Question
        fields = "__all__"
