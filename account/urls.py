from django.urls import path,include
from rest_framework import routers

from .views import UserViewSet,CreateUser,UserProfileView,CustomAuthToken, UserFollow
router = routers.DefaultRouter()

router.register('users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('create-user/', CreateUser.as_view(), name='create-user'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', CustomAuthToken.as_view(), name="login"),
    path('follow/<int:pk>/', UserFollow.as_view(), name='user-follow'),
]
