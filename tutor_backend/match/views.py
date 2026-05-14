from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from match.models import Match
from match.serializers import MatchDetailSerializer, MatchListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.
@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_or_create_match(request):
    if request.method == "GET":
        user=request.user
        if user.role=='student':
            matches = Match.objects.filter(student=request.user).order_by('-created_at')
        elif user.role=='teacher':
            matches=Match.objects.filter(teacher__user=request.user).order_by('-created_at')
        else:
            matches=Match.objects.all()

        serializer = MatchListSerializer(matches, many=True)
        return Response(
            {"message": "匹配列表获取成功", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    """创建匹配接口：学生提交匹配请求"""
    if request.method == 'POST':
        serializer = MatchDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)  # 自动关联当前登录的学生用户
            return Response(
                {"message": "匹配创建成功", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "匹配创建失败", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def match_detail(request, pk):
    """匹配详情接口：学生查看匹配详情，教师接单/完成匹配"""
    try:
        match = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return Response(
            {"message": "匹配不存在"},
            status=status.HTTP_404_NOT_FOUND
        )
    #不是这个匹配的老师或者学生就拒接访问
    if match.student != request.user and match.teacher.user != request.user:
            return Response(
                {"message": "你没有权限查看这个匹配"},
                status=status.HTTP_403_FORBIDDEN
            )
    serializer = MatchDetailSerializer(match)
    return Response(
        {"message": "匹配详情获取成功", "data": serializer.data},
        status=status.HTTP_200_OK
    )

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def match_confirm(request, pk):
    """匹配确认接口：教师确认匹配请求"""
    try:
        match = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return Response(
            {"message": "匹配不存在"},
            status=status.HTTP_404_NOT_FOUND
        )
    #只有这个匹配的老师才能确认
    if match.teacher.user != request.user:
            return Response(
                {"message": "你没有权限确认这个匹配"},
                status=status.HTTP_403_FORBIDDEN
            )
    if match.status != 'pending':
        return Response(
            {"message": "只有待处理的匹配才能被确认"},
            status=status.HTTP_400_BAD_REQUEST
        )
    match.status = 'confirmed'
    match.save()
    serializer = MatchDetailSerializer(match)
    return Response(
        {"message": "匹配确认成功", "data": serializer.data},
        status=status.HTTP_200_OK
    )