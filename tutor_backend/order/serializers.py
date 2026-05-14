from rest_framework import serializers
from order.models import Order
class OrderDetailSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    teacher_username = serializers.CharField(source='teacher.user.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    teacher_username = serializers.CharField(source='teacher.user.username', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'student_username', 'teacher_username', 'subject', 'scheduled_time', 'duration', 'price', 'address', 'remarks']