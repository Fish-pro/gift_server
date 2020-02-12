#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
import uuid

from utils.model_choices import GENDER_CHOICES, WORK_TYPE_CHOICES


class UUIDTools(object):
    """
    生成uuid
    """

    @staticmethod
    def uuid4_hex():
        return uuid.uuid4().hex


class BaseModle(models.Model):
    """
    共有属性
    """
    uuid = models.CharField(primary_key=True, max_length=64, unique=True, default=UUIDTools.uuid4_hex)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True)
    status = models.IntegerField(default=1) # 1启用 2禁用 3删除

    class Meta:
        abstract = True

class User(BaseModle):
    '''用户表'''
    name = models.CharField(max_length=64, null=True) # 姓名
    address = models.CharField(max_length=255,null=True) # 地区
    gender = models.IntegerField(choices=GENDER_CHOICES, default=3) # 1男 2女 3未知
    age = models.IntegerField(default=0) # 年龄
    isManager = models.BooleanField(default=False) # 是否是管理员

    class Meta:
        db_table = 'tb_user'

class Work(BaseModle):
    '''事务表'''
    userUuid = models.CharField(max_length=64, null=True) # 事务人
    type = models.IntegerField(choices=WORK_TYPE_CHOICES, default=1) # 1婚宴 2白事 3.其他
    name = models.CharField(max_length=64, null=True) # 事务名称
    startTime = models.BigIntegerField(null=True) # 开始时间
    endTime = models.BigIntegerField(null=True) # 结束时间

    remarks = models.CharField(max_length=1024, null=True) # 事务备注

    class Meta:
        db_table = 'tb_work'

class UserWork(BaseModle):
    '''送礼记录表'''
    name = models.CharField(max_length=64, null=True) # 送礼人姓名
    remarks = models.CharField(max_length=244, null=True) # 备注
    workUuid = models.CharField(max_length=64, null=True) # 事务uuid
    money = models.BigIntegerField(null=True) # 送礼金额
    quilt = models.IntegerField(default=0) # 被子数量 默认0
    woollen = models.IntegerField(default=0) # 毛毯数量 默认0
    fireworks = models.IntegerField(default=0) # 烟花数量 默认0
    artillery = models.IntegerField(default=0) # 火炮数量 默认0
    wreath = models.IntegerField(default=0) # 花圈数量 默认0

    class Meta:
        db_table = 'tb_user_work'

class UserAuth(BaseModle):
    '''认证登录表'''
    userUuid = models.ForeignKey('User', models.CASCADE, null=True, related_name='userAuthkUuid', to_field='uuid')
    tel = models.CharField(max_length=64, null=True) # 电话
    password = models.CharField(max_length=255, null=True) # 密码

    class Meta:
        db_table = 'tb_user_auth'

class LoginLog(BaseModle):
    """登录日志"""
    ipAddr = models.CharField(max_length=126, verbose_name='IP地址', null=True)
    userUuid = models.CharField(max_length=64, null=True)
    userAgent = models.CharField(max_length=256, verbose_name='登录平台', null=True)
    isManager = models.BooleanField(default=False)  # 0 客户端登录  1 是后台管理端

    class Meta:
        db_table = 'tb_login_log'
