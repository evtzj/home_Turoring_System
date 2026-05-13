
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from user.serializers import RegisterSerializer,LoginSerializer,UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def register_view (request):
    serializer =RegisterSerializer(data=request.data)
    if  serializer.is_valid():
        user =serializer.save()
        return Response(
            {
                "message":"注册成功",
                "data":{
                    "username":user.username,
                    "id":user.id,
                    "phone":user.phone,
                    "role":user.role,
                }
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "message":"注册失败",
            "errors":serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def login_view(request):
    serializer=LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "message":"参数错误","errors":serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user=serializer.validated_data["user"]
    
    token, _=Token.objects.get_or_create(user=user)
    return Response(
        {
            "message":"登录成功",
            "data":{
                "token":token.key,
                "id":user.id,
                "username":user.username,
                "phone":user.phone,
                "role":user.role
            }
        },
        status=status.HTTP_200_OK
    )
@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user

    if request.method == "GET":
        serializer = UserProfileSerializer(user)
        return Response(
            {"message": "获取个人信息成功", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "修改个人信息成功", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    
    return Response(
        {"message": "参数错误", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    user = request.user
    Token.objects.filter(user=user).delete()
    return Response(
        {"message":"退出成功"},
        status=status.HTTP_200_OK
    )
    