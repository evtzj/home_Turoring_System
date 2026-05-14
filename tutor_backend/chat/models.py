from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class ChatMessage(models.Model):
    match = models.ForeignKey('match.Match',on_delete=models.CASCADE)
    sender = models.ForeignKey('user.User',on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
