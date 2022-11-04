from rest_framework import viewsets
from .models import Profile, About
from .serializers import ProfileSerializers, AboutSerializers
from rest_framework.permissions import IsAuthenticated


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)


class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializers
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)
