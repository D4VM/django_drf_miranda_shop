from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
