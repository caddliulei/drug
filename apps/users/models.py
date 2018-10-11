# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=10, null=True, blank=True, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='邮箱')
    work_org = models.CharField(max_length=20, default='', verbose_name='工作单位')
    research_dir = models.CharField(max_length=20, default='', verbose_name='研究方向')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __unicode__(self):
        return self.username


class VerifyCode(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField(max_length=6, verbose_name='验证码')
    email = models.CharField(max_length=100, verbose_name='邮箱')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code



