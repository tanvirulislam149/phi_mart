from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"   # For using email instead of username
    REQUIRED_FIELDS = []       # no field required like username

    objects = CustomUserManager()

    def __str__(self):
        return self.email 

