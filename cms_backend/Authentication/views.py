from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, LoginSerializer
from Authentication.permissions import IsAdminOrReadOnly
# Helper function to generate tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignUpAPIView(APIView):
    """This API will handle signup"""
    # permission_classes = [IsAdminOrReadOnly]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # tokens = get_tokens_for_user(user)

            return Response({
                "user_id": user.id,
                "username": user.username,
                "role": user.groups.all()[0].id if user.groups.exists() else None,
                # "tokens": tokens
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """This API will handle login and return JWT tokens"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "username": user.username,
                    "role": user.groups.all()[0].id if user.groups.exists() else None,
                    "tokens": tokens
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Username or Password",
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
