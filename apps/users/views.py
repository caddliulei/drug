# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import choice
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets
from .serializers import EmailSerializer, UserRegSerializer
from .models import VerifyCode
from utils import email_send
User = get_user_model()

# Create your views here.


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class EmailCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """
    serializer_class = EmailSerializer

    def generate_code(self):
        """
        生成六位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = self.generate_code()
        email_status = email_send.email_send(email=email, code=code)

        if email_status == 1:
            code_record = VerifyCode(code=code, email=email)
            code_record.save()
            return Response({
                "email": email
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "email": email_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)


class UserRegViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    """
    serializer_class = UserRegSerializer


# class UserForgetPWDViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

