import django_filters

from manager.models import User, Work, UserWork


class UsersFilter(django_filters.FilterSet):
    """用户filters"""
    name = django_filters.CharFilter("name", lookup_expr="icontains")  # 姓名模糊匹配
    address = django_filters.CharFilter("address", lookup_expr="icontains")  # 地址模糊匹配

    class Meta:
        model = User
        fields = "__all__"

class WorksFilter(django_filters.FilterSet):
    """用户filters"""
    userUuid = django_filters.CharFilter("userUuid", lookup_expr="exact")
    name = django_filters.CharFilter("name", lookup_expr="icontains")  # 姓名模糊匹配

    class Meta:
        model = Work
        fields = "__all__"

class UserWorksFilter(django_filters.FilterSet):
    """用户filters"""
    workUuid = django_filters.CharFilter("userUuid", lookup_expr="exact")
    name = django_filters.CharFilter("name", lookup_expr="icontains")  # 姓名模糊匹配

    class Meta:
        model = UserWork
        fields = "__all__"
