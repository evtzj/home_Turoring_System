from django.db import models

# Create your models here.
class Order(models.Model):
    student = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='orders')
    teacher = models.ForeignKey('user.TeacherProfile', on_delete=models.CASCADE, related_name='orders')
    subject = models.CharField(max_length=100)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField(help_text='Duration in minutes')
    status = models.CharField(max_length=20, default='pending')  # pending, confirmed, completed, cancelled
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.student.username} with {self.teacher.user.username}"