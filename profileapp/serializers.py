from rest_framework import serializers
from .models import Profile, About


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class AboutSerializers(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"
