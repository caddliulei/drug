# coding=utf-8
from __future__ import unicode_literals
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from .models import VerifyCode
from works.models import AutoDuck
from drug.settings import reg_email

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

    def validate_email(self, email):
        """
        验证邮箱是否注册
        """

        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("用户邮箱已经存在")
        # 验证邮箱号码是否合法
        if not re.match(reg_email, email):
            raise serializers.ValidationError("邮箱号码非法")
        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, email=email).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return email


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(email=self.initial_data["email"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        verify_records = VerifyCode.objects.filter(email=self.initial_data["email"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            print five_mintes_ago
            print last_record.add_time
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email', 'code', 'mobile', 'work_org', 'research_dir', 'password')


class UserforgetPWSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)

    def validate_email(self, email):
        """
        验证邮箱是否注册
        """

        # 邮箱是否注册
        if not User.objects.filter(email=email).count():
            raise serializers.ValidationError("用户邮箱不存在")
        # 验证邮箱号码是否合法
        if not re.match(reg_email, email):
            raise serializers.ValidationError("邮箱号码非法")
        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, email=email).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return email
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    password1 = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码1", label="密码1", write_only=True,
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码2", label="密码1", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserforgetPWSerializer, self).create(validated_data=validated_data)
        if validated_data["password1"] == validated_data["password2"]:
            user.set_password(validated_data["password1"])
            user.save()
            return user

    def validate(self, attrs):
        del attrs["code"]
        del attrs["password1"]
        del attrs["password2"]
        return attrs

    class Meta:
        model = User
        fields = ('email', 'code', 'password1', 'password2')



