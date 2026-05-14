from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import ChatMessage
from chat.serializers import ChatSerializer
from user.models import User
from user.serializers import UserProfileSerializer
from match.models import Match
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_users(request):
    if request.user.role != 'admin':
        return Response(
            {"message":"你没有权限查看用户列表"},
            status=status.HTTP_403_FORBIDDEN
        )
    users = User.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(
        {"message":"用户列表获取成功","data":serializer.data},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    if request.user.role != 'admin':
        return Response(
            {"message":"你没有权限查看用户列表"},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {"message":"用户不存在"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = UserProfileSerializer(user)
    return Response(
        {"message":"用户详情获取成功","data":serializer.data},
        status=status.HTTP_200_OK
    )
#审核教师资格接口：管理员审核教师资格
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_teacher(request, pk):
    if request.user.role != 'admin':
        return Response(
            {"message":"你没有权限审核教师资格"},
            status=status.HTTP_403_FORBIDDEN
        )
    try:
        teacher = User.objects.get(pk=pk, role='teacher')
    except User.DoesNotExist:
        return Response(
            {"message":"教师不存在"},
            status=status.HTTP_404_NOT_FOUND
        )
    teacher.is_verified = True
    teacher.save()
    return Response(
        {"message":"教师资格审核成功"},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def count_stats(request):
    if request.user.role != 'admin':
        return Response(
            {"message":"你没有权限查看统计数据"},
            status=status.HTTP_403_FORBIDDEN
        )
    total_users = User.objects.count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_students = User.objects.filter(role='student').count()
    total_messages = ChatMessage.objects.count()
    total_matches = Match.objects.count()
    data = {
        "total_users": total_users,
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_messages": total_messages,
        "total_matches": total_matches,
    }
    return Response(
        {"message":"统计数据获取成功","data":data},
        status=status.HTTP_200_OK
    )