
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    last_login = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} {self.email}"
