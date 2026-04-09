from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员'),
    )

    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name='身份类型')
    is_verified = models.BooleanField(default=False, verbose_name='是否认证')

    def __str__(self):
        return self.username


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teaching_years = models.IntegerField(default=0, verbose_name='教龄')
    subject = models.CharField(max_length=100, verbose_name='授课科目')
    education = models.CharField(max_length=100, blank=True, null=True, verbose_name='学历')
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True, verbose_name='资质证书')
    id_card_image = models.ImageField(upload_to='id_cards/', blank=True, null=True, verbose_name='身份证图片')

    def __str__(self):
        return f"{self.user.username} 的教师信息"