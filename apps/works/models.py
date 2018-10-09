# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from drug.settings import MEDIA_ROOT
User = get_user_model()

# Create your models here.


def upload_to(instance, filename):
    return '/'.join([MEDIA_ROOT, instance.user.username, instance.work_name, filename])


class Banner(models.Model):
    """
    首页轮播图
    """
    image = models.ImageField(upload_to='media/banner/', verbose_name="轮播图片")
    index = models.IntegerField(verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "轮播图"


class Product(models.Model):
    """
    服务内容
    """
    name = models.CharField(max_length=20, verbose_name='服务名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '服务内容'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class AutoDuck(models.Model):
    """
    分子对接  用户指点中心坐标以及盒子大小

    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    mol_db = models.CharField(max_length=10, choices=((1, 'zinc'), (2, 'chembl')), verbose_name='数据库选择')
    size_x = models.FloatField(verbose_name='size_x')
    size_y = models.FloatField(verbose_name='size_y')
    size_z = models.FloatField(verbose_name='size_z')
    center_x = models.FloatField(verbose_name='center_x')
    center_y = models.FloatField(verbose_name='center_y')
    center_z = models.FloatField(verbose_name='center_z')
    pdb_file = models.FileField(upload_to=upload_to, verbose_name='pdb文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '分子对接'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


class AutoDuck2(models.Model):
    """
    分子对接  用户指点对接的残基

    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    mol_db = models.CharField(max_length=10, choices=((1, 'zinc'), (2, 'chembl')), verbose_name='数据库选择')
    lig_file = models.FileField(upload_to=upload_to, verbose_name='配体文件')
    pdb_file = models.FileField(upload_to=upload_to, verbose_name='pdb文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '分子对接2'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


class VirtualScreen(models.Model):
    """
    虚拟筛选
    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    mol_db = models.CharField(max_length=10, choices=((1, 'zinc'), (2, 'chembl')), verbose_name='数据库选择')
    size_x = models.FloatField(verbose_name='size_x')
    size_y = models.FloatField(verbose_name='size_y')
    size_z = models.FloatField(verbose_name='size_z')
    center_x = models.FloatField(verbose_name='center_x')
    center_y = models.FloatField(verbose_name='center_y')
    center_z = models.FloatField(verbose_name='center_z')
    pdb_file = models.FileField(upload_to=upload_to, verbose_name='pdb文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '虚拟筛选'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


class VirtualScreen2(models.Model):
    """
    虚拟筛选2
    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    mol_db = models.CharField(max_length=10, choices=((1, 'zinc'), (2, 'chembl')), verbose_name='数据库选择')
    lig_file = models.FileField(upload_to=upload_to, verbose_name='残基文件')
    pdb_file = models.FileField(upload_to=upload_to, verbose_name='pdb文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '虚拟筛选2'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


class VsBlast(models.Model):
    """
    VsleadBlast
    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    sequence = models.CharField(max_length=1000, verbose_name='蛋白序列')
    protein_db = models.CharField(max_length=10, choices=((1, 'zinc'), (2, 'chembl')))
    e_value = models.CharField(max_length=10, choices=((1, 0.00001), (2, 0.0001), (3, 0.001),
                                                       (4, 0.01), (5, 0.01), (6, 1), (7, 10)),
                               verbose_name='E值选择')
    out_format = models.CharField(max_length=10, choices=((1, 'pariwise'), (2, 'XML blast output'),
                                                          (3, 'tabular')), verbose_name='输出格式选择')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = 'VsleadBlast'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


class ReverseVirtualScreen(models.Model):
    """
    反向虚拟筛选
    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    target_db = models.CharField(max_length=10, choices=((1, 'zine'), (2, 'chembl')), verbose_name='靶点数据库')
    mol_file = models.FileField(upload_to=upload_to, verbose_name='靶点文件')
    top_n = models.IntegerField(verbose_name='返回结果数目')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '反向虚拟筛选'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


class Dynamic(models.Model):
    """
    动力学模拟
    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    conf_info = models.CharField(max_length=20, choices=((1, '通用计算'), (2, '计算结合能'), (3, '计算氢键'),
                                                         (4, '聚类分析')), verbose_name='配置信息')
    protein_file = models.FileField(upload_to=upload_to, verbose_name='蛋白文件')
    mol_file = models.FileField(upload_to=upload_to, verbose_name='小分子文件')
    conf_project = models.CharField(max_length=100, choices=((1, '有水'), (2, '无水'), (3, '自计算')),
                                    verbose_name='配置项目')
    s_file = models.FileField(upload_to=upload_to, default='', verbose_name='S信息文件')
    lig_file = models.FileField(upload_to=upload_to, default='', verbose_name='lig文件')
    frcmod_file = models.FileField(upload_to=upload_to, default='', verbose_name='frcmod文件')
    res_num = models.IntegerField(default=0, verbose_name='氨基酸数目')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '动力学模拟'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username


class Admet(models.Model):
    """
    ADMET预测
    """
    user = models.ForeignKey(User, verbose_name='用户')
    work_name = models.CharField(max_length=20, verbose_name='任务名称')
    work_decs = models.CharField(max_length=100, default='', verbose_name='任务描述')
    mol_file = models.FileField(upload_to=upload_to, verbose_name='小分子文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = 'ADMET预测'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username

