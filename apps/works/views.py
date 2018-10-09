# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Banner, Product
from .serializers import BannerSerializer, ProductSerializer, AutoDuckSerializer,  VirtualScreenSerializer
from .serializers import VsBlastSerializer, ReverseVirtualScreenSerializer, DynamicSerializer, AdmetSerializer
from .serializers import AutoDuck2Serializer, VirtualScreen2Serializer
from .tasks import duck_perform, duck2_perform, screen_perform, screen2_perform

# Create your views here.


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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AutoDuckViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    保存对接数据
    """
    serializer_class = AutoDuckSerializer
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
        file_path = '/home/jianping/pywork/drug/media/%s/%s' % (username, work_name)
        duck_perform.delay(center_x, center_y, center_z, size_x, size_y, size_z, mol_db, pdb_file, file_path)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AutoDuck2Viewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    保存对接数据
    """
    serializer_class = AutoDuck2Serializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        username = request.user.username
        work_name = request.data['work_name']
        mol_db = request.data['mol_db']
        lig_file = request.data['lig_file'].name
        pdb_file = request.data['pdb_file'].name
        lig_file = '/home/jianping/pywork/drug/media/%s/%s/%s' % (username, work_name, lig_file)
        file_path = '/home/jianping/pywork/drug/media/%s/%s' % (username, work_name)
        duck2_perform.delay(mol_db, lig_file, pdb_file, file_path)
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
        file_path = '/home/jianping/pywork/drug/media/%s/%s' % (username, work_name)
        screen_perform.delay(center_x, center_y, center_z, size_x, size_y, size_z, mol_db, pdb_file, file_path)
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
        lig_file = request.data['lig_file'].name
        pdb_file = request.data['pdb_file'].name
        lig_file = '/home/jianping/pywork/drug/media/%s/%s/%s' % (username, work_name, lig_file)
        file_path = '/home/jianping/pywork/drug/media/%s/%s' % (username, work_name)
        screen2_perform.delay(mol_db, lig_file, pdb_file, file_path)
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
