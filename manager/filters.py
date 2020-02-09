import django_filters

from manager.models import User


class UsersFilter(django_filters.FilterSet):
    """用户filters"""
    name = django_filters.CharFilter("name", lookup_expr="icontains")  # 姓名模糊匹配
    address = django_filters.CharFilter("address", lookup_expr="icontains")  # 地址模糊匹配

    class Meta:
        model = User
        fields = "__all__"
