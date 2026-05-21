from rest_framework import serializers
from chat.models import ChatMessage

class ChatSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username',read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['id','match','sender','sender_username','content','created_at']
        read_only_fields = ['match','sender','created_at']