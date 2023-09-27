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
from utils.helper import Employee_id


class SignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


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
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"msg:No Data found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user_id = request.user.id
        user_profile = UserProfile.objects.get(user_id=user_id)
        profile_serializer = UserProfileSerializer(instance=user_profile, data=request.data)

        if not profile_serializer.is_valid():
            return Response({"msg: data you entered is wrong"}, status=status.HTTP_400_BAD_REQUEST
                            )
        profile_serializer.save()
        return Response(profile_serializer.data)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        password = serializer.initial_data["password"]
        phone = serializer.initial_data["phone_number"]
        user = authenticate(request, phone_number=phone, password=password)
        if not user:
            return Response({"msg: wrong Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
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
            profile_serializer = UserProfileSerializer(instance=user_profile, data=request.data)

            if not profile_serializer.is_valid():
                return Response({"msg": "please enter correct data"}, status=status.HTTP_400_BAD_REQUEST
                                )
            profile_serializer.save()
            return Response({"msg": "Data Updated Successfully"}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                "msg": "user with this id does not exists"
            }, status=status.HTTP_404_NOT_FOUND)


class CreateView(APIView):
    permission_classes = [IsAuthenticated, RequiredAdmin | RequiredManager]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST
                            )
        serializer.save()
        return Response(serializer.data)


class ManagerCreateProfileView(APIView):
    permission_classes = [IsAuthenticated, RequiredManager]

    def post(self, request):
        try:
            user_id = request.POST.get("user")
            if not Employee_id(user_id):
                return Response(
                    {"msg": "You Don't Have Permission For This Access"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            serializer = UserProfileSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"msg": "Profile created successfully"})
        except Exception:
            return Response({"msg": "Incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
