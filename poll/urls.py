from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PollListCreatedByUserViewSet

router = DefaultRouter()
router.register('poll-list', PollListCreatedByUserViewSet, basename='poll-list')

urlpatterns = [
    path('', include(router.urls)),
]