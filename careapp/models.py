from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserRegistration(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username
    

class NurseRegistration(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    password = models.CharField(max_length=50)
    
