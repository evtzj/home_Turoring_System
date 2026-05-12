from rest_framework import serializers
from user.models import User

class LoginSerializer(serializers.Serializer):
        #设置手机号和账号名都可以登录
        account=serializers.CharField(max_length=20)
        password= serializers.CharField(write_only=True)
        #先尝试账号登陆,如果账号不存在再尝试手机号登录
        def validate(self,data):
            account = data.get("account")
            password = data.get("password")

            user = User.objects.filter(username=account).first()
            if user is None:
                user = User.objects.filter(phone=account).first()
                if user is None:
                    raise serializers.ValidationError("账号不存在")
            
            if not user.check_password(password):
                raise serializers.ValidationError("密码错误")
            
            data["user"]=user
            return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True, allow_blank=False)
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
    
    def validate_username(self,value):
        if value and len(value)>20:
            raise serializers.ValidationError("用户名不能超过20个字符")
        if value and User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已经被占用了")
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
            username=validated_data.get("username") or validated_data["phone"],
            phone=validated_data["phone"],
            password=validated_data["password"],
            role=validated_data["role"],
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "phone", "role", "is_verified", "email", "first_name", "last_name"]
        read_only_fields = ["id", "phone", "role", "is_verified"]