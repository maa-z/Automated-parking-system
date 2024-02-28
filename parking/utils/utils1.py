from home.models import * 
from django.utils import timezone

users = CustomUser.objects.all()
cars = Cars.objects.all()
parking = Parking.objects.all()
slots = Slots.objects.all()

def entry(number):
    car = Cars.objects.filter(car_number=number)
    if car.exists():
        user = car.user
        if user.balance>0:
            p = Parking.objects.create(car=car,entry=timezone.now())
            return True
        else:
            return False
    else:
        return False

def exit(number):
    car = Cars.objects.filter(car_number=number)
    p = Parking.objects.filter(car=car,exit=None)
    p.exit = timezone.now()
    total_time_seconds = (p.exit - p.entry).seconds
    total_time_min = (total_time_seconds//60) + 1
    total_cost = total_time_min * 5
    p.cost = total_cost
    p.save()
    user = car.user 
    user.balance = user.balance - total_cost
    user.save()



