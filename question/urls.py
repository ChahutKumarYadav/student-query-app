from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet,AnswerViewSet

router = DefaultRouter()
router.register("question", QuestionViewSet, basename='question')
router.register("answer", AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
]
