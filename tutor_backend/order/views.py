from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from order.models import Order
from order.serializers import OrderDetailSerializer, OrderListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    """创建订单接口：学生提交订单请求"""
    serializer = OrderDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(student=request.user)  # 自动关联当前登录的学生用户
        return Response(
            {"message": "订单创建成功", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"message": "订单创建失败", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )

