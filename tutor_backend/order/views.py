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
@api_view(['POST'],['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_or_create_order(request):
    if request.method == 'GET':
        user=request.user
        if user.role=='student':
            orders = Order.objects.filter(student=request.user).order_by('-created_at')
        elif user.role=='teacher':
            orders=Order.objects.filter(teacher__user=request.user).order_by('-created_at')
        else:
            orders=Order.objects.all()

        serializer = OrderListSerializer(orders, many=True)
        return Response(
            {"message": "订单列表获取成功", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    """创建订单接口：学生提交订单请求"""
    if request.method == 'POST':
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
    

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def list_orders(request):
#     """订单列表接口：学生查看自己的订单列表"""
   

@api_view(['GET'],['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """订单详情接口：学生查看订单详情，教师接单/完成订单"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "订单不存在"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = OrderDetailSerializer(order)
        return Response(
            {"message": "订单详情获取成功", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    if request.method == 'PUT':
        # 只有教师可以接单或完成订单
        if request.user.role != 'teacher':
            return Response(
                {"message": "只有教师可以修改订单状态"},
                status=status.HTTP_403_FORBIDDEN
            )
        # 教师只能修改自己相关的订单
        if order.teacher.user != request.user:
            return Response(
                {"message": "你没有权限修改这个订单"},
                status=status.HTTP_403_FORBIDDEN
            )
        # 更新订单状态
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"message": "无效的订单状态"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = OrderDetailSerializer(order)
        return Response(
            {"message": "订单状态更新成功", "data": serializer.data},
            status=status.HTTP_200_OK
        )