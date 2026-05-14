from rest_framework import serializers
from match.models import Match
class MatchDetailSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    teacher_username = serializers.CharField(source='teacher.user.username', read_only=True)

    class Meta:
        model = Match
        fields = '__all__'


class MatchListSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    teacher_username = serializers.CharField(source='teacher.user.username', read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'student_username', 'teacher_username', 'subject', 'created_at', 'status']