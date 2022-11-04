from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from .views import ProfileViewSet,AboutViewSet

router = routers.DefaultRouter()
router.register('user_profile', ProfileViewSet)
router.register('about',AboutViewSet)

urlpatterns = [
    path('', include(router.urls))]
