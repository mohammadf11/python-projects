from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from random import randint
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import User, VerifyCode, Profile
from social_media.models import Follow
from . import serializers
from . import permissions


class UserRegisterApiView(APIView):
    authentication_classes = []
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            data = serializer_data.validated_data
            self.request.session['user_info_api'] = {
                'phone_number': data['phone_number'],
                'email': data['email'],
                'password': data['password2'],
            }
            code = randint(10000, 99999)

            VerifyCode.objects.filter(
                phone_number=data['phone_number']).delete()
            VerifyCode.objects.create(
                phone_number=data['phone_number'], code=code)

            return Response(serializer_data.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyCodeApiView(APIView):
    authentication_classes = []
    serializer_class = serializers.UserVerifycodeSerializer

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            data = serializer_data.validated_data
            user_info = request.session['user_info_api']
            verify_code_instance = VerifyCode.objects.get(
                phone_number=user_info['phone_number'])

            if verify_code_instance.code == data['code']:
                user = User.objects.create_user(
                    phone_number=user_info['phone_number'],
                    email=user_info['email'],
                    password=user_info['password'],
                )
                del request.session['user_info_api']
                VerifyCode.objects.filter(
                    phone_number=data['phone_number']).delete()
                return Response(serializer_data.data, status=status.HTTP_200_OK)
            else:
                return Response({'messages': 'code is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInformationsApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserInformationsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(id=self.request.user.id)


class UserInformationsModelViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserInformationsSerializer
    permission_classes = [IsAuthenticated , permissions.IsStaffAccessPermissions]


class ProfileInformationsModelViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffAccessPermissions]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffOrOwnerAccessPermissions]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
