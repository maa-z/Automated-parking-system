from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
# from django.db import models
from parking import settings

class CustomUser(AbstractUser):
    balance = models.IntegerField(default=500)



# Create your models here.

class Cars(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null=True, blank=True)
    car_name = models.CharField(max_length=100)
    car_number = models.CharField(max_length=100,unique=True)

    def __str__(self) -> str:
        return self.car_name


class Parking(models.Model):
    car = models.ForeignKey(Cars,on_delete=models.SET_NULL , null=True,blank=True)
    entry = models.DateTimeField()
    exit = models.DateTimeField(null=True)
    cost = models.IntegerField(null=True)

class Slots(models.Model):
    total_slot = models.IntegerField()
    booked_slot = models.IntegerField()

class Spots(models.Model):
    car = models.ForeignKey(Cars,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=100)
    available = models.BooleanField()
    #entry 
    entry = models.DateTimeField(null=True,blank=True)
    #exit
    # exit = models.DateTimeField(null=True)





    
  