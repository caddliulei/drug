# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import choice
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets
from dynamic_rest.viewsets import DynamicModelViewSet
from dynamic_rest.pagination import DynamicPageNumberPagination
from utils.permissions import IsOwnerOrReadOnly
from works.models import AutoDock, AutoDock2, VirtualScreen, VirtualScreen2
from .serializers import EmailSerializer, UserRegSerializer, AutoDuckOrderSerializer, AutoDuck2OrderSerializer,\
    VirtualScreenOrderSerializer, VirtualScreen2OrderSerializer, UserDetailSerializer, PasswordresetSerializer

from .models import VerifyCode
from utils import email_send
User = get_user_model()

# Create your views here.


class OrdersPagination(DynamicPageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"


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


class UserinfoViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    用户详情
    """
    serializer_class = UserDetailSerializer
    # queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)


class AutoDockOrderViewset(DynamicModelViewSet):
    """
    订单管理
    list:
        获取个人订单
    """
    queryset = AutoDock.objects.all()
    pagination_class = OrdersPagination
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AutoDuckOrderSerializer
    ordering = ('-add_time',)


class AutoDock2OrderViewset(DynamicModelViewSet):
    """
    订单管理
    list:
        获取个人订单
    """
    queryset = AutoDock2.objects.all()
    pagination_class = OrdersPagination
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AutoDuck2OrderSerializer
    ordering = ('-add_time',)


class VirtualScreenOrderViewset(DynamicModelViewSet):
    """
    订单管理
    list:
        获取个人订单
    """
    queryset = VirtualScreen.objects.all()
    pagination_class = OrdersPagination
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = VirtualScreenOrderSerializer
    ordering = ('-add_time',)


class VirtualScreen2OrderViewset(DynamicModelViewSet):
    """
    订单管理
    list:
        获取个人订单
    """
    queryset = VirtualScreen2.objects.all()
    pagination_class = OrdersPagination
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = VirtualScreen2OrderSerializer
    ordering = ('-add_time',)


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class PasswordresetViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordresetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        email = request.data['email']
        password = request.data['password']
        user = User.objects.get(email=email)
        user.password = make_password(password)
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
