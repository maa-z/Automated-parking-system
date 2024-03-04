from django.shortcuts import render , redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from home.models import *

# TOTAL_SLOT = 10
# BOOKED_SLOT = 0

# because you add abstract user model
User = get_user_model()

# Create your views here.

def home(request):
    parkings = Parking.objects.filter(car__user=request.user)
    parkings = parkings.order_by('-entry')
    return render(request,'home/home.html',{'title':"Parking",'parkings':parkings})



def login_page(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')

        if not User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO, "Invalid Username")
            return redirect('/login')
        
        user = authenticate(username = username , password = password)
        if user is None:
            messages.add_message(request, messages.INFO, "Invalid Password")
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/')
    return render(request,'home/login.html',{'title':"login"})



def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(first_name,username,password)

        user = User.objects.filter(username = username)
        if user.exists():

            messages.add_message(request, messages.INFO, "User Name Already exists")
            return redirect('/register')

        user = User.objects.create(
            first_name = first_name,
            username = username      
        )
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.INFO, "Successfully created user")
        return redirect('/login')

    return render(request,'home/register.html',{'title':"register"})



def logout_page(request):
    logout(request)
    return redirect('/login')


def cars(request):
    if request.method == "POST":
        car_name = request.POST.get('name')
        car_number = request.POST.get('number')
        user = CustomUser.objects.filter(username=request.user.username)[0]

        car = Cars.objects.filter(car_number = car_number)
        slot = Slots.objects.all()[0]
        # print(slot)
        if slot.total_slot==slot.booked_slot:
            messages.add_message(request, messages.INFO, "No Slot Available")
            return redirect('/cars')
        if car.exists():
            messages.add_message(request, messages.INFO, "Car Number Already exists")
            return redirect('/cars')


        slot.booked_slot = slot.booked_slot+1
        slot.save()
        # print(slot.parked)
        car = Cars.objects.create(
            user = user,
            car_name = car_name,
            car_number = car_number      
        )
        car.save()
        # print("cars save")
        messages.add_message(request, messages.INFO, "Successfully car added")
        return redirect('/cars')
    cars = Cars.objects.filter(user=request.user)
    context = {'cars':cars,'title':"cars"}
    return render(request,'home/cars.html',context)

def account(request):
    if request.method == "POST":
        amount = request.POST.get("money")
        request.user.balance = int(amount)+request.user.balance
        request.user.save()
        return redirect('/account')
    return render(request,'home/account.html',{'title':"account"})


def parking(request):
    return render(request,'home/parking.html')