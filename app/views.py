from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializerls import (
    UserSerializer, LoginSerializer, UserProfileSerializer
)
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from utils.decorators import RequiredAdmin, RequiredManager
from utils.helper import employee_id
from utils.msg import *


class SignUpView(APIView):
    def post(self, request):
        role = request.data["role"]
        if role == "A":
            return Response(unauthorised, status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)


class ProfileSignUpView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user_id = request.user.id
        try:
            user = UserProfile.objects.get(user=user_id)
            serializer = UserProfileSerializer(user, context={'request': request})
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(no_data, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user_id = request.user.id
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
            profile_serializer = UserProfileSerializer(
                instance=user_profile, data=request.data, context={'request': request}
            )

            if not profile_serializer.is_valid():
                return Response(wrong_data, status=status.HTTP_400_BAD_REQUEST
                                )
            profile_serializer.save()
            return Response(profile_serializer.data)
        except UserProfile.DoesNotExists:
            return Response(no_data, status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        password = serializer.initial_data["password"]
        phone = serializer.initial_data["phone_number"]
        user = authenticate(request, phone_number=phone, password=password)
        if not user:
            return Response(
                wrong_cred, status=status.HTTP_401_UNAUTHORIZED
            )
        Refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(Refresh),
            "access": str(Refresh.access_token)
        }
        )


class AdminAccessView(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated, RequiredAdmin]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated, RequiredAdmin]

    def put(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(user_id=pk)
            profile_serializer = UserProfileSerializer(
                instance=user_profile,
                data=request.data,
                context={'request': request}
            )

            if not profile_serializer.is_valid():
                return Response(
                    wrong_data, status=status.HTTP_400_BAD_REQUEST
                                )
            profile_serializer.save()
            return Response(
                success, status=status.HTTP_200_OK
            )
        except UserProfile.DoesNotExist:
            return Response({
                wrong_data
            }, status=status.HTTP_404_NOT_FOUND)


class CreateView(APIView):
    permission_classes = [IsAuthenticated, RequiredAdmin | RequiredManager]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
                            )
        serializer.save()
        return Response(serializer.data)


class ManagerCreateProfileView(APIView):
    permission_classes = [IsAuthenticated, RequiredManager]

    def post(self, request):
        try:
            user_id = request.POST.get("user")
            if not employee_id(user_id):
                return Response(
                    unauthorised,
                    status=status.HTTP_401_UNAUTHORIZED
                )
            serializer = UserProfileSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(success)
        except Exception:
            return Response(
                wrong_data, status=status.HTTP_400_BAD_REQUEST
            )
