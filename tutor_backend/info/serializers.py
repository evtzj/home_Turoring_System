from rest_framework import serializers
from user.models import User, TeacherProfile


class TeacherListSerializer(serializers.ModelSerializer):
    """老师列表用的序列化器 —— 只要关键信息，不用全部返回"""
    username = serializers.CharField(source='user.username', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ['id', 'username', 'phone', 'subject', 'teaching_years', 'education']


class TeacherDetailSerializer(serializers.ModelSerializer):
    """老师详情用的序列化器 —— 返回完整信息"""
    username = serializers.CharField(source='user.username', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    is_verified = serializers.BooleanField(source='user.is_verified', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = '__all__'
