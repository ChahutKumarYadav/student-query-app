from rest_framework import serializers
from .models import User, UserFollowing
from question.serializers import QuestionSerializer, AnswerSerializer
from profileapp.serializers import ProfileSerializers, AboutSerializers
from poll.serializers import PollQuestionSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    user_profile = ProfileSerializers(read_only=True)
    user_about = AboutSerializers(read_only=True)
    answered_question = AnswerSerializer(read_only=True, many=True)
    question_asked = QuestionSerializer(read_only=True, many=True)
    poll = PollQuestionSerializer(read_only=True, many=True)

    class Meta:
        model = User
        exclude = ("password",)

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data


class FollowingSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='following_user_id.email')

    class Meta:
        model = UserFollowing
        fields = ['id', 'following_user_id', 'email', 'created']


class FollowersSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user_id.email')

    class Meta:
        model = UserFollowing
        fields = ['id', 'user_id', 'email', 'created']


class MiniUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']
