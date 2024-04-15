from django.db import models
from django.contrib.auth.models import User
from autherization.models import *
# Create your models here.



class NurseBooking(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE,related_name='Nurse',null=True, default=0)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE,related_name='user', null=True, default=0)
    date = models.DateField()
    duration = models.IntegerField() 
    is_active = models.BooleanField(default=False, null=True)
    created_at = models.DateField(auto_now_add=True)
    # has_requested = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return self.user.username





class Report(models.Model):
    user = models.ForeignKey(NurseBooking, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    details = models.TextField()