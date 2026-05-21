from django.db import models

# Create your models here.
class TeacherFavorite(models.Model):
    student = models.ForeignKey('user.User', on_delete=models.CASCADE)
    teacher = models.ForeignKey('user.TeacherProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'teacher')