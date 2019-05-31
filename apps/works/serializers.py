# coding=utf-8
# from __future__ import unicode_literals

from rest_framework import serializers
from dynamic_rest.serializers import DynamicModelSerializer
from .models import Banner, Product, AutoDock, AutoDock2, VirtualScreen, VirtualScreen2, SeaTarget, SeaVirScreen
from .models import Target, VsBlast, ReverseVirtualScreen, Dynamic, Admet, Screen, Dock, VirScreen, Gbsa
from django.contrib.auth import get_user_model

User = get_user_model()


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class TargetSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Target
        fields = '__all__'


class AutoDockSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = AutoDock
        fields = "__all__"


class AutoDock2Serializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = AutoDock2
        fields = "__all__"


class VirtualScreenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = VirtualScreen
        fields = "__all__"


class VirtualScreen2Serializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = VirtualScreen2
        fields = "__all__"


class VsBlastSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = VsBlast
        fields = "__all__"


class ScreenSerializer(DynamicModelSerializer):

    class Meta:
        model = Screen
        fields = "__all__"


class ReverseVirtualScreenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ReverseVirtualScreen
        fields = "__all__"


class DynamicSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Dynamic
        fields = "__all__"


class AdmetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Admet
        fields = "__all__"


class DockSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Dock
        fields = "__all__"


class DockOrderSerializer(DynamicModelSerializer):

    class Meta:
        model = Dock
        fields = "__all__"


class VirScreenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = VirScreen
        fields = "__all__"


class SeaTargetOrderSerializer(DynamicModelSerializer):

    class Meta:
        model = SeaTarget
        fields = "__all__"


class SeaVirScreenOrderSerializer(DynamicModelSerializer):

    class Meta:
        model = SeaVirScreen
        fields = "__all__"


class VirScreenOrderSerializer(DynamicModelSerializer):

    class Meta:
        model = VirScreen
        fields = "__all__"


class GbsaSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Gbsa
        fields = "__all__"


class GbsaorderSerializer(DynamicModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Gbsa
        fields = "__all__"
