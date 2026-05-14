from django.db import models

# Create your models here.
class Match(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )

    student = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='matches_as_student')
    teacher = models.ForeignKey('user.TeacherProfile', on_delete=models.CASCADE, related_name='matches_as_teacher')
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending',choices=STATUS_CHOICES)  # pending, confirmed, completed, cancelled
    def __str__(self):
        return f"Match {self.id} - {self.student.username} with {self.teacher.user.username}"