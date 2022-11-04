from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers as slr
from poll.models import PollQuestion
from .serializers import PollQuestionSerializer


class PollListCreatedByUserViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PollQuestion.objects.all()
    serializer_class = PollQuestionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(owner=self.request.user)
        json_data = slr.serialize("json", queryset)
        return JsonResponse(json_data, safe=False)
