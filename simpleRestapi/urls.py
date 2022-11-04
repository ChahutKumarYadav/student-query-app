from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/search/', include('search_api.urls')),
    path('api/question/', include('question.urls')),
    path('api/poll/', include('poll.urls')),
    # path('api/answer/', include('answer.urls')),
    path('api/profile/',include('profileapp.urls')),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
