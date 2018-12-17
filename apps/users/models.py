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
    name = models.CharField(max_length=10, null=True, blank=True, verbose_name='username')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='email')
    work_org = models.CharField(max_length=20, default='', verbose_name='work_org')
    research_dir = models.CharField(max_length=20, default='', verbose_name='research_dir')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __unicode__(self):
        return self.username


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField(max_length=6, verbose_name='code')
    email = models.CharField(max_length=100, verbose_name='email')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code


class Passwordreset(models.Model):
    email = models.EmailField(max_length=100, verbose_name='email')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')
