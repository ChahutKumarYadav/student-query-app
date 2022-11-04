from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from .serializers import UserSerializer, RegistrationSerializer, UserLoginSerializer
import json
from .models import User, UserFollowing


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CreateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(json.dumps({
                "success": 1,
                "message": "Successfully account created",
                "user_detail": serializer.data}))
        else:
            return Response(json.dumps({"success": 0, "message": serializer.errors}))


class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# class SendPasswordResetEmailView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         serializer = SendPasswordResetEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserFollow(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise ValueError

    def get(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
        except Exception:
            return Response({'message': 'User does not exists '})
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        # user = User.objects.get(pk=request.data['user'])
        user = request.user
        try:
            follow = self.get_object(pk)
        except Exception:
            return Response({'message': 'User does not exists '})
        try:
            if user != follow:
                UserFollowing.objects.create(user_id=user, following_user_id=follow)
            else:
                return Response({"message": "You can't follow yourself"})
        except Exception as e:
            return Response({"message": f"You already follow {follow}"})

        # serializer = UserSerializer(follow)
        return Response({'message': f'You follow {follow}'})

    # unfollow users.
    def delete(self, request, pk, format=None):
        # user = User.objects.get(pk=request.data['user'])
        user = request.user
        try:
            follow = self.get_object(pk)
        except Exception:
            return Response({'message': 'User does not exists '})
        try:
            connection = UserFollowing.objects.filter(user_id=user, following_user_id=follow).first()
            connection.delete()
        except Exception:
            return Response({'message': f"You don't follow {follow}"})
        # serializer = UserSerializer(follow)
        return Response({'message': f'You unfollowed {follow}'})


# To see following and followers of all the users.
# class UserFollowingViewSet(viewsets.ModelViewSet):
#     queryset = UserFollowing.objects.all()
#     serializer_class = U
#     http_method_names = ['get']

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'delete']

    @action(detail=True, methods=['GET'])
    def no_of_follow(self, request, pk=None, format=None):
        user = User.objects.get(id=pk)
        return Response({"no_followers": len(UserSerializer(user).data['followers']),
                         "no_following": len(UserSerializer(user).data['following'])})
