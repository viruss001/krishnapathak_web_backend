
from django.db import models
from django.contrib.auth.models import User  
from django.utils import timezone
from datetime import timedelta

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"

def default_expiry():
    return timezone.now() + timedelta(minutes=20)

class Otp(models.Model):
    otp = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    exp = models.DateTimeField(default=default_expiry)  # use DateTimeField for exact expiry

    def is_expired(self):
        return timezone.now() > self.exp