from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {"username": {"detail": "User Doesnot exist!"}}
            if User.objects.filter(email=request.data["email"]).exists():
                user = User.objects.get(email=request.data["email"])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    "success": True,
                    "email": user.email,
                    "token": token.key,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "user": serializer.data,
                "token": Token.objects.get(
                    user=User.objects.get(email=serializer.data["email"])
                ).key,
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK
        )
