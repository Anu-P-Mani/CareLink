from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from autherization.models import *
from clinical_devices.models import *
from medicines.models import *
from django.core.validators import RegexValidator

# Create your models here.

class Divicecart(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    device=models.ForeignKey(DeviceInformation,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity*self.device.price


class Order(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    device_id=models.ForeignKey(DeviceInformation,on_delete=models.CASCADE)

    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    no_of_items = models.PositiveIntegerField(default=1)
    order_status=models.CharField(max_length=30,default="pending")
    delivary_status=models.CharField(max_length=30,default="pending")
    address=models.CharField(max_length=200)
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message='Phone number must be 10 digits')])

class Medcart(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    medicine=models.ForeignKey(Medicine_inventory,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity*self.medicine.price
    
class MedicineOrder(models.Model):

    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    medicine=models.ForeignKey(Medicine_inventory,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    no_of_items = models.PositiveIntegerField(default=1)
    order_status=models.CharField(max_length=30,default="pending")
    delivary_status=models.CharField(max_length=30,default="pending")
    address=models.CharField(max_length=200)
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message='Phone number must be 10 digits')])



class Account(models.Model):
    accnumber=models.IntegerField()
    acctype=models.CharField(max_length=200)
    balance=models.IntegerField()


    def __str__(self):
        return str (self.accnumber)
