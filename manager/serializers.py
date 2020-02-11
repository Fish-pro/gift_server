from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import serializers

from manager.model_choices import GENDER_CHOICES
from manager.models import User, UserWork, Work, UserAuth
from utils.errors import ParamError
from utils.return_info import USER_AREADY_EXIST, TEL_AREADY_EXIST


class UserSerializer(serializers.ModelSerializer):
    '''用户序列化表'''

    class Meta:
        model = User
        fields = ('uuid', 'name', 'address', 'gender', 'age', 'status')

class UserPostserializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=2,
                                 max_length=10,
                                 required=True,
                                 error_messages={
                                     'min_length': "姓名最少两个字符",
                                     'max_length': "姓名最多10个字符"})
    address = serializers.CharField(min_length=2,
                                    max_length=30,
                                    required=True,
                                    error_messages={
                                        'min_length': "地址最少两个字符",
                                        'max_length': "地址最多30个字符",})
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True,
                                     error_messages={"required": "课程介绍必填"})
    age = serializers.IntegerField(max_value=150, min_value=0,
                                             error_messages={"required": "年龄必填", "min_value": "年龄有误",
                                                             "max_value": "年龄有误"})
    tel = serializers.CharField(min_length=2,
                                max_length=30,
                                required=True,
                                error_messages={"required": "手机号必填"})
    password = serializers.CharField(min_length=6,
                                     max_length=12,
                                     required=True,
                                     error_messages={
                                         'min_length': "密码最少两个字符",
                                         'max_length': "密码最多12个字符"})

    def validate(self, data):
        checkUser = User.objects.filter(name=data["name"], address=data["address"],status=1).first()
        if checkUser:
            raise ParamError(USER_AREADY_EXIST)
        checkTel = UserAuth.objects.filter(tel=data["tel"]).first()
        if checkTel:
            raise ParamError(TEL_AREADY_EXIST)
        return data

    def create_user(self, validated_data):
        user_dict= {}
        user_dict["name"] = validated_data["name"]
        user_dict["address"] = validated_data["address"]
        user_dict["gender"] = validated_data["gender"]
        user_dict["age"] = validated_data["age"]
        user = User.objects.create(**user_dict)
        return user

    def create_user_auth(self, validated_data, user):
        auth_dict = {}
        auth_dict["tel"] = validated_data["tel"]
        auth_dict["userUuid"] = user
        auth_dict["password"] = make_password(validated_data["password"])
        auth = UserAuth.objects.create(**auth_dict)
        return auth

    class Meta:
        model = User
        fields = ('uuid', 'name', 'address', 'gender', 'age', 'status', "tel", "password")

class UserWorkSerializer(serializers.ModelSerializer):
    '''用户送礼表'''

    class Meta:
        model = UserWork
        fields = ('uuid', 'name', 'address', 'money', 'quilt', 'woollen', 'fireworks', 'artillery', 'wreath', 'status')

class WorkSerializer(serializers.ModelSerializer):
    '''事务表'''

    totalMoney = serializers.SerializerMethodField()

    def get_totalMoney(self, obj):
        allMoney = UserWork.objects.annotate(num_money=Sum('money')).filter(workUuid=obj).values('money')
        return allMoney[0]['num_money']

    class Meta:
        model = Work
        fields = ('uuid', 'user', 'type', 'name', 'startTime', 'endTime', 'remarks')