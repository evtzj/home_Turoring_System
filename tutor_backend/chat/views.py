from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import ChatMessage
from chat.serializers import ChatSerializer
from match.models import Match
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat_of_match(request,match_id):
    if request.method == "GET":
        message = ChatMessage.objects.filter(match_id=match_id).order_by('created_at')
        if message.count()==0:
            return Response(
                {"message":"没有聊天记录"},
                status=status.HTTP_200_OK
            )
        serializer = ChatSerializer(message,many=True)
        return Response(
            {"message":"查找聊天记录成功","data":serializer.data},
            status=status.HTTP_200_OK
        )
    
    if request.method == "POST":
        match = Match.objects.get(pk=match_id)
        if match.student != request.user and match.teacher.user != request.user:
            return Response(
                {"message":"你无权发消息"},
                status=403
            )
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message":"...","errors":serializer.errors},status=400)
        
        serializer.save(sender=request.user,match=match)
        return Response({"message":"发送成功","data":serializer.data},status=201)
