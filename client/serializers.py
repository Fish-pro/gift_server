from django.db.models import Sum
from rest_framework import serializers

from manager.models import User, UserWork, Work


class UserSerializer(serializers.ModelSerializer):
    '''用户序列化表'''

    class Meta:
        model = User
        fields = ('uuid', 'name', 'address', 'gender', 'age', 'status')

class UserWorkSerializer(serializers.ModelSerializer):
    '''用户送礼表'''
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.userUuid, many=False).data

    def get_ownerUsesr(self, obj):
        return

    class Meta:
        model = UserWork
        fields = ('uuid', 'user', 'money', 'quilt', 'woollen', 'fireworks', 'artillery', 'wreath', 'status')

class WorkSerializer(serializers.ModelSerializer):
    '''事务表'''

    totalMoney = serializers.SerializerMethodField()

    def get_totalMoney(self, obj):
        allMoney = UserWork.objects.annotate(num_money=Sum('money')).filter(workUuid=obj).values('money')
        return allMoney[0]['num_money']

    class Meta:
        model = Work
        fields = ('uuid', 'user', 'type', 'name', 'startTime', 'endTime', 'remarks')