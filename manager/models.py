#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
import uuid

def get_uuid():
    """
    生成数据库uuid
    :return:
    """
    return "".join(str(uuid.uuid4()).split("-")).upper()

class BaseModle(models.Model):
    """
    共有属性
    """
    uuid = models.CharField(max_length=64, default=get_uuid(), unique=True)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True)
    status = models.IntegerField(default=1) # 1启用 2禁用 3删除

    class Meta:
        abstract = True

class User(BaseModle):
    '''用户表'''
    name = models.CharField(max_length=64, null=True) # 姓名
    address = models.CharField(max_length=255,null=True) # 地区
    gender = models.IntegerField(default=3) # 1男 2女 3未知
    age = models.IntegerField(default=0) # 年龄

    class Meta:
        db_table = 'tb_user'

class Work(BaseModle):
    '''事务表'''
    userUuid = models.ForeignKey('User', models.CASCADE, null=True, related_name='userWorkUuid', to_field='uuid') #事务人
    type = models.IntegerField(default=1) # 1婚宴 2白事 3.其他
    name = models.CharField(max_length=64, null=True) # 事务名称
    startTime = models.BigIntegerField(null=True) # 开始时间
    endTime = models.BigIntegerField(null=True) # 结束时间
    remarks = models.CharField(max_length=1024) # 事务备注
    createUserUuid = models.ForeignKey('User', models.CASCADE, null=True, related_name='createUserWorkUuid', to_field='uuid') #事务人

    class Meta:
        db_table = 'tb_work'

class UserWork(BaseModle):
    '''送礼记录表'''
    userUuid = models.ForeignKey('User', models.CASCADE, null=True, related_name='userToWorkUuid', to_field='uuid')
    workUuid = models.ForeignKey('Work', models.CASCADE, null=True, related_name='workUserUuid', to_field='uuid')
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
    userUuid = models.ForeignKey('User', models.CASCADE, null=True, related_name='longinLogUuid', to_field='uuid')
    userAgent = models.CharField(max_length=256, verbose_name='登录平台', null=True)
    isManager = models.BooleanField(default=False)  # 0 客户端登录  1 是后台管理端

    class Meta:
        db_table = 'tb_login_log'
