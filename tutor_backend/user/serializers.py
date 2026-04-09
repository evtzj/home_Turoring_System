from rest_framework import serializers
from user.models import User

class LoginSerializer(serializers.Serializer):
        phone=serializers.CharField(max_length=20)
        password= serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code =serializers.CharField(max_length=6)
    password=serializers.CharField(write_only=True,min_length=6)
    role=serializers.ChoiceField(choices=['student','teacher'])

    def validate_phone(self,value):
        if not value.isdigit() or len(value) !=11:
            raise serializers.ValidationError("手机号得是11位数的")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("手机号已经被注册了")
        return value
    
    def validate_code(self,value):
        #先格式校验，再接入短信验证码服务
        if not value.isdigit() or len(value)!=6:
            raise serializers.ValidationError('验证码必须是6位数')
        return value
    
    def create(self,validated_data):
        phone =validated_data["phone"]
        password = validated_data["password"]
        role = validated_data["role"]

        user = User.objects.create_user(
            username=phone,
            phone=phone,
            password=password,
            role=role,
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "phone", "role", "is_verified", "email", "first_name", "last_name"]
        read_only_fields = ["id", "phone", "role", "is_verified"]