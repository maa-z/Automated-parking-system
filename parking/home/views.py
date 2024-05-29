from django.shortcuts import render , redirect , HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from home.models import *
from django.utils import timezone

from django.contrib.auth.decorators import login_required
# Create your views here.


# TOTAL_SLOT = 10
# BOOKED_SLOT = 0

# because you add abstract user model
User = get_user_model()

# Create your views here.
@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def logout_page(request):
    logout(request)
    return redirect('/login')

@login_required(login_url="/login/")
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





# from instamojo_wrapper import Instamojo
# from django.conf import settings

# api = Instamojo(api_key=settings.API_KEY, auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')



@login_required(login_url="/login/")
def account(request):
    if request.method == "POST":
        amount = request.POST.get("money")
        request.user.balance = int(amount)+request.user.balance
        request.user.save()
        return redirect(f'/account/money/{amount}')
    return render(request,'home/account.html',{'title':"account"})


@login_required(login_url="/login/")
def money(request,amount):

    # response = api.payment_request_create(
    #     amount = amount,
    #     purpose = 'Order Process',
    #     buyer_name = request.user.first_name,
    #     email = 'thisishaque3@gmail.com',
    #     redirect_url = ' http://127.0.0.1:8000/account'
    # )
    # print(response)
    
    return render(request,'home/money.html',{'title':"pay",'money':amount})









@login_required(login_url="/login/")
def parking(request):

    if 'button' in request.GET:
        button_clicked = request.GET['button']

        # spot = Spots.objects.filter(id=button_clicked)[0]
        
        # if spot.availabel:  # empyty
        #     spot.available = False 
        #     spot.entry = timezone.now()
        #     pass 
        # else: # not empty
        #     pass

        return HttpResponse(f"You clicked {button_clicked}")

    return render(request,'home/parking.html',{'spots':Spots.objects.all()})




def entry_exit(request,id):
    return HttpResponse(f"hello {id}")




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            # print("hello")
            data = json.loads(request.body)
            # print(data)
            data = int(data['car_no'])
            car = Cars.objects.filter(car_number=data)
            if len(car): # car is registered 
                print("car registerd")
                car = car[0]
                spot = Spots.objects.filter(car=car)
                if len(spot): ## exit
                    print("exit")
                    spot = spot[0]
                    entry_time = spot.entry 
                    user = car.user
                    exit_time = timezone.now()
                    total_time = (exit_time-entry_time).seconds
                    total_time_min = (total_time//60)+1
                    money = total_time_min * 50
                    user.balance = user.balance-money
                    user.save()

                    p = Parking.objects.create(
                        car = car,
                        entry = entry_time,
                        exit = exit_time,
                        cost = money
                    )
                    p.save()

                    spot.car = None 
                    spot.entry = None 
                    spot.available = True 
                    spot.save()

                    slot = Slots.objects.all()[0]
                    slot.booked_slot = slot.booked_slot-1
                    slot.save()

                else: ## entry
                    print("entery")
                    ## check user have balance
                    balance = car.user.balance
                    if balance>0:
                        print("have balance")
                        ## check slot  is empty 
                        slot = Slots.objects.all()[0]
                        if slot.total_slot > slot.booked_slot: # slot empty 
                            print("slot available")
                            ## any empty spot 
                            slot.booked_slot = slot.booked_slot+1
                            slot.save()

                            spot_empty = Spots.objects.filter(car=None)[0]
                            spot_empty.car = car 
                            spot_empty.available = False
                            spot_empty.entry = timezone.now()
                            spot_empty.save()

                            # return redirect('/')
                        else: # slot not empty
                            pass
                    else:# no balance 
                        pass
            else: # not registerd car
                pass

            # Process the data
            # For example, access data fields like this:
            # field_value = data.get('field_name')

            # Perform operations with the data

            response = {
                'status': True,
                
                'message': 'Data received successfully test',
                # 'data': data  # Optional: echo received data back in response
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON test'}, status=400)
    else:
        return JsonResponse({'status': False, 'message': 'Invalid request method test'}, status=405)
