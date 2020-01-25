from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Create your models here.


class DJUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=20)
