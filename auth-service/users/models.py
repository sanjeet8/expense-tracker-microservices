from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')

    class Meta:
        swappable = 'AUTH_USER_MODEL'  # Ensure Django recognizes this as a swappable user model

    def __str__(self):
        return f"{self.username} - {self.role}"