from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import serializers

from utils.model_choices import GENDER_CHOICES, WORK_TYPE_CHOICES
from manager.models import User, UserWork, Work, UserAuth
from utils.errors import ParamError
from utils.return_info import USER_AREADY_EXIST, TEL_AREADY_EXIST, USER_NOT_EXIST, WORK_NOT_EXIST


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
        checkTel = UserAuth.objects.filter(tel=data["tel"], status=1).first()
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

class UserUpdateserializer(serializers.ModelSerializer):

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
                                     error_messages={"required": "性别必填"})
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


    def check_data(self, data, uuid):
        checkUser = User.objects.exclude(uuid=uuid).filter(name=data["name"], address=data["address"], status=1).first()
        if checkUser:
            raise ParamError(USER_AREADY_EXIST)
        checkTel = UserAuth.objects.exclude(userUuid__uuid=uuid).filter(tel=data["tel"]).first()
        if checkTel:
            raise ParamError(TEL_AREADY_EXIST)
        return data

    def update_user(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.address = validated_data.get("address")
        instance.gender = validated_data.get("gender")
        instance.age = validated_data.get("age")
        instance.save()
        return instance

    def update_auth(self, instance, validated_data):
        auth = instance.userAuthkUuid.first()
        auth.tel = validated_data.get("tel")
        auth.password = make_password(validated_data.get("password"))
        auth.save()
        return auth

    class Meta:
        model = User
        fields = ('uuid', 'name', 'address', 'gender', 'age', 'status', "tel", "password")

class WorkSerializer(serializers.ModelSerializer):
    '''事务表'''

    totalMoney = serializers.SerializerMethodField()

    def get_totalMoney(self, obj):
        allMoney = UserWork.objects.annotate(num_money=Sum('money')).filter(workUuid=obj.uuid).values('money')
        if len(allMoney) == 0:
            return 0
        return allMoney[0]['num_money']

    class Meta:
        model = Work
        fields = ('userUuid', 'uuid', 'type', 'name', 'startTime', 'endTime', 'remarks', 'totalMoney')


class WorkPostserializer(serializers.ModelSerializer):

    userUuid = serializers.CharField(min_length=2,
                                     max_length=64,
                                     required=True,
                                     error_messages={
                                        "required": "事务用户必填"})

    name = serializers.CharField(min_length=2,
                                 max_length=50,
                                 required=True,
                                 error_messages={
                                     'min_length': "姓名最少两个字符",
                                     'max_length': "姓名最多50个字符",
                                     "required": "名称必填"})

    type = serializers.ChoiceField(choices=WORK_TYPE_CHOICES, required=True,
                                     error_messages={"required": "事务类型必填"})

    startTime = serializers.IntegerField(required=True,
                                         error_messages={
                                             "required": "开始时间必填"})
    endTime = serializers.IntegerField(required=True,
                                       error_messages={
                                            "required": "结束时间必填"})
    remarks = serializers.CharField(required=False)

    def validate(self, data):
        userUuid = data["userUuid"]
        user = User.objects.filter(uuid=userUuid,status=1).first()
        if not user:
            raise ParamError(USER_NOT_EXIST)
        return data

    def create_work(self, validated_data):
        work = Work.objects.create(**validated_data)
        return work

    def update_work(self, instance, validate_data):
        instance.userUuid = validate_data.get('userUuid')
        instance.type = validate_data.get('type')
        instance.name = validate_data.get('name')
        instance.startTime = validate_data.get('startTime')
        instance.endTime = validate_data.get('endTime')
        instance.remarks = validate_data.get('remarks')
        instance.save()
        return instance

    class Meta:
        model = Work
        fields = ('userUuid', 'type', 'name', 'startTime', 'endTime', 'remarks')


class UserWorkSerializer(serializers.ModelSerializer):
    '''用户送礼表'''

    class Meta:
        model = UserWork
        fields = ('workUuid', 'uuid', 'name', 'remarks', 'money', 'quilt', 'woollen', 'fireworks', 'artillery', 'wreath', 'status')

class UserWorkPostserializer(serializers.ModelSerializer):

    workUuid = serializers.CharField(min_length=2,
                                     max_length=64,
                                     required=True,
                                     error_messages={
                                        "required": "事务必填"})
    name = serializers.CharField(min_length=2,
                                 max_length=50,
                                 required=True,
                                 error_messages={
                                     'min_length': "姓名最少两个字符",
                                     'max_length': "姓名最多50个字符",
                                     "required": "送礼人姓名必填"})
    remarks = serializers.CharField(required=False)
    money = serializers.IntegerField(required=True,
                                     error_messages={"required": "送礼金额必填"})
    quilt = serializers.IntegerField(required=True,
                                     error_messages={"required": "被子数量必填"})
    woollen = serializers.IntegerField(required=True,
                                     error_messages={"required": "毛毯数量必填"})
    fireworks = serializers.IntegerField(required=True,
                                     error_messages={"required": "烟花数量必填"})
    artillery = serializers.IntegerField(required=True,
                                     error_messages={"required": "火炮数量必填"})
    wreath = serializers.IntegerField(required=True,
                                     error_messages={"required": "花圈数量必填"})

    def validate(self, data):
        work = Work.objects.filter(uuid=data["workUuid"],status=1).first()
        if not work:
            raise ParamError(WORK_NOT_EXIST)
        return data

    def create_user_work(self,validate_data):
        user_work = UserWork.objects.create(**validate_data)
        return user_work

    def update_user_work(self,instance,validate_data):
        instance.name = validate_data.get("name")
        instance.remarks = validate_data.get("remarks")
        instance.workUuid = validate_data.get("workUuid")
        instance.money = validate_data.get("money")
        instance.quilt = validate_data.get("quilt")
        instance.woollen = validate_data.get("woollen")
        instance.fireworks = validate_data.get("fireworks")
        instance.artillery = validate_data.get("artillery")
        instance.wreath = validate_data.get("wreath")
        instance.save()
        return instance

    class Meta:
        model = UserWork
        fields = ('workUuid', 'name', 'remarks', 'money', 'quilt', 'woollen', 'fireworks', 'artillery', 'wreath')