# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from dynamic_rest.viewsets import DynamicModelViewSet
from .models import Banner, Product, Screen
from users.views import OrdersPagination
from utils.permissions import IsOwnerOrReadOnly
from .serializers import BannerSerializer, ProductSerializer, AutoDockSerializer,  VirtualScreenSerializer
from .serializers import VsBlastSerializer, ReverseVirtualScreenSerializer, DynamicSerializer, AdmetSerializer
from .serializers import AutoDock2Serializer, VirtualScreen2Serializer, ScreenSerializer
from .tasks import perform_dock, perform_dock2, perform_screen, perform_screen2, perform_screen_user, perform_screen2_user
from drug.settings import BASE_DIR
# Create your views here.


class ScreenPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 10


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class ProductViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Product.objects.all().order_by("-add_time")
    serializer_class = ProductSerializer


class AutoDockViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存对接数据
    """
    serializer_class = AutoDockSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        username = request.user.username
        work_name = request.data['work_name']
        size_x = request.data['size_x']
        size_y = request.data['size_y']
        size_z = request.data['size_z']
        center_x = request.data['center_x']
        center_y = request.data['center_y']
        center_z = request.data['center_z']

        pdb_file = request.data['pdb_file'].name
        lig_file = request.data['lig_file'].name
        pdb_path = os.path.join(BASE_DIR, 'media', 'dock', username, work_name, pdb_file)  # (username, work_name)
        lig_path = os.path.join(BASE_DIR, 'media', 'dock', username, work_name, lig_file)
        res_path = os.path.join(BASE_DIR, 'media', 'dock', username, work_name)
        perform_dock.delay(work_name, center_x, center_y, center_z, size_x, size_y, size_z, pdb_path, lig_path, res_path)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AutoDock2Viewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存对接数据
    """
    serializer_class = AutoDock2Serializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        username = request.user.username
        work_name = request.data['work_name']
        pdb_file = request.data['pdb_file'].name
        lig_file = request.data['lig_file'].name
        resi_file = request.data['resi_file'].name
        pdb_path = os.path.join(BASE_DIR, 'media', 'dock2', username, work_name, pdb_file)  # (username, work_name)
        lig_path = os.path.join(BASE_DIR, 'media', 'dock2', username, work_name, lig_file)
        resi_path = os.path.join(BASE_DIR, 'media', 'dock2', username, work_name, resi_file)
        res_path = os.path.join(BASE_DIR, 'media', 'dock2', username, work_name)
        perform_dock2.delay(work_name, pdb_path, lig_path, resi_path, res_path)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VirtualScreenViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存虚拟筛选数据
    """
    serializer_class = VirtualScreenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        username = request.user.username
        work_name = request.data['work_name']
        size_x = request.data['size_x']
        size_y = request.data['size_y']
        size_z = request.data['size_z']
        center_x = request.data['center_x']
        center_y = request.data['center_y']
        center_z = request.data['center_z']
        mol_db = request.data['mol_db']
        pdb_file = request.data['pdb_file'].name
        user_db = request.data['user_db']
        pdb_path = os.path.join(BASE_DIR, 'media', 'screen', username, work_name, pdb_file)
        res_path = os.path.join(BASE_DIR, 'media', 'screen', username, work_name)
        if user_db == '':
            perform_screen.delay(work_name, center_x, center_y, center_z, size_x, size_y, size_z, mol_db, pdb_path,
                                 res_path)
        else:
            user_db_name = request.data['user_db'].name
            perform_screen_user.delay(work_name, center_x,
                                      center_y, center_z, size_x, size_y, size_z, user_db_name,
                                      pdb_path, res_path)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VirtualScreen2Viewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存虚拟筛选数据
    """
    serializer_class = VirtualScreen2Serializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        username = request.user.username
        work_name = request.data['work_name']
        mol_db = request.data['mol_db']
        resi_file = request.data['resi_file'].name
        pdb_file = request.data['pdb_file'].name
        pdb_path = os.path.join(BASE_DIR, 'media', 'screen2', username, work_name, pdb_file)
        resi_path = os.path.join(BASE_DIR, 'media', 'screen2', username, work_name, resi_file)
        res_path = os.path.join(BASE_DIR, 'media', 'screen2', username, work_name)
        user_db = request.data['user_db']
        if user_db == '':
            perform_screen2.delay(work_name, mol_db, pdb_path, resi_path, res_path)
        else:
            user_db_name = request.data['user_db'].name
            perform_screen2_user.delay(work_name, user_db_name,  pdb_path, resi_path, res_path)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VsBlastViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存VsleadBlast
    """
    serializer_class = VsBlastSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ReverseVirtualScreenViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存反向虚拟筛选数据
    """
    serializer_class = ReverseVirtualScreenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class DynamicViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存动力学数据
    """
    serializer_class = DynamicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AdmetViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    保存admet数据
    """
    serializer_class = AdmetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ScreenViewset(DynamicModelViewSet):
    """
    筛选订单结果
    list:
        获取个人订单结果
    """
    queryset = Screen.objects.all()
    pagination_class = OrdersPagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ScreenSerializer
    ordering = ('work_name',)


