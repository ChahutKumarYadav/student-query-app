from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SearchQuestionViewSet

router = DefaultRouter()
router.register('question', SearchQuestionViewSet, basename='question')


urlpatterns = [
    path('', include(router.urls)),
]
