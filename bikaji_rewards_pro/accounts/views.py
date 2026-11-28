from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdministrator
from .serializers import UserCreateSerializer


User = get_user_model()


class AddUserView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "User created successfully.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "User creation failed.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class AdminUserCountView(APIView):

    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication
    ]

    permission_classes = [
        IsAuthenticated,
        IsAdministrator
    ]

    def get(self, request):

        total_users = User.objects.count()

        return Response(
            {
                "message": "User count retrieved successfully.",
                "total_users": total_users
            },
            status=status.HTTP_200_OK
        )
