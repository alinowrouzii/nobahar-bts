from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # email = models.CharField(unique=True,blank=False, null=False ,max_length=50)
    name = models.CharField(max_length=50, default="")
    def __str__(self):
        return f"{self.email} - {self.name}"