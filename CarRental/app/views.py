from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from .models import *
import os
# Create your views here.
def car_login(req):
    if 'shop' in req.session:
                return redirect(shop_home)
    if 'user' in req.session:
            return redirect(user_home)
    if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            shop=authenticate(username=uname,password=password)
            if shop:
                    login(req,shop)
                    if shop.is_superuser:
                            req.session['shop']=uname   
                            return redirect(shop_home)
                    else:
                            req.session['user']=uname   
                            return redirect(user_home)
            else:
                messages.warning(req,'Invaild username or password!!!')
                return redirect(car_login)
    else:
            return render(req,'login.html')

def register(req):
    if req.method=='POST':
        email=req.POST['email']
        uname=req.POST['uname']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=password)
            data.save()
        #     send_mail('Registration In EcommShop', 'Successfully Registered In EcommShop', settings.EMAIL_HOST_USER, [email])
            return redirect(car_login)
        except:
            messages.warning(req,'Email Already Exists!!')
            return redirect(register)
    else:
        return render(req,'register.html')


def car_logout(req):
    logout(req)
    req.session.flush()
    return redirect(car_login)
    
# ___________________________________________________________________________ADMIN__________________________________________________________________________________________

def shop_home(req):
        data=Cars.objects.all() 
        return render(req,'shop/shop.html',{'data':data})

# def addcars(req):
#         if 'shop' in req.session:
#                 if req.method=='POST':
#                         cid=req.POST['cid']
#                         model=req.POST['model']
#                         make=req.POST['p_makes']
#                         year=req.POST['year']
#                         color=req.POST['color']
#                         license_plate=req.POST['license_plate']
#                         mileage=req.POST['mileage']
#                         price_per_day=req.POST['price_per_day']
#                         description=req.POST['description']
#                         is_available=req.POST['is_available']== 'on'
#                         image=req.FILES['image']
#                         data=Cars.objects.create( cid=cid,model=model,make=Makes.objects.get(makes=make),year=year,color=color,license_plate=license_plate,mileage=mileage,price_per_day= price_per_day,description=description, is_available=is_available,image=image)
#                         data.save()
#                         return redirect(shop_home)
#                 else:
#                         data=Makes.objects.all()       
#                         return render(req,'shop/addcars.html',{'data':data})
#         else:
#                 return redirect(car_login)

def addcars(req):
    if req.method == 'POST':
        car_id = req.POST.get('cid')
        make = req.POST.get('p_makes')
        model = req.POST.get('model')
        year = req.POST.get('year')
        body_type = req.POST.get('body_type')
        fuel = req.POST.get('fuel')
        transmission = req.POST.get('transmission')
        mileage = req.POST.get('mileage')
        price_per_day = req.POST.get('price_per_day')
        description = req.POST.get('description')
        image = req.FILES.get('image')

        try:
            if not car_id or not model or not year or not mileage or not price_per_day or not image:
                raise ValidationError("All required fields must be filled.")
            
            if float(price_per_day) <= 0:
                raise ValidationError("Price per day must be greater than 0.")
            
            Cars.objects.create(
               cid=car_id,
                make=Makes.objects.get(makes=make),
                model=model,
                year=year,
                bodytype=body_type,
                fuel=fuel,
                transmission=transmission,
                mileage=mileage,
                price_per_day=price_per_day,
                description=description,
                image=image
            )
            return redirect(shop_home)

        except ValidationError as e:
            error_message = e.message
            return render(req, 'shop/addcars.html', {'error_message': error_message, 'data': data})

    else:
        data = Makes.objects.all()
        return render(req, 'shop/addcars.html', {'data': data})

def makess(req):
        if 'shop' in req.session:
                if req.method == 'POST':
                        make=req.POST['p_makes']
                        data=Makes.objects.create(makes=make)
                        data.save()
                        return redirect(makess)
                else:
                        data=Makes.objects.all()
                        return render(req,'shop/make.html',{'data':data})
        else:
                return redirect(car_login)
# ___________________________________________________________________________ADMIN_________________________________________________________________________________________
def user_home(req):
    # if req.method == 'POST':
    #     # Access form data directly from req.POST
    #     pickup_location = req.POST.get('pickup-location')
    #     pickup_date = req.POST.get('pickup-date')
    #     pickup_hour = req.POST.get('pickup-hour')
    #     pickup_minute = req.POST.get('pickup-minute')
    #     pickup_ampm = req.POST.get('pickup-ampm')
        
    #     dropoff_location = req.POST.get('dropoff-location')
    #     dropoff_date = req.POST.get('dropoff-date')
    #     dropoff_hour = req.POST.get('dropoff-hour')
    #     dropoff_minute = req.POST.get('dropoff-minute')
    #     dropoff_ampm = req.POST.get('dropoff-ampm')

    #     # Combine the hour, minute, and AM/PM into a full time string (24-hour format)
    #     pickup_time_str = f"{pickup_hour}:{pickup_minute} {pickup_ampm}"
    #     dropoff_time_str = f"{dropoff_hour}:{dropoff_minute} {dropoff_ampm}"

    #     # Convert time to 24-hour format for storing in the database
    #     pickup_time = datetime.strptime(pickup_time_str, "%I:%M %p").time()
    #     dropoff_time = datetime.strptime(dropoff_time_str, "%I:%M %p").time()

    #     # Save the booking to the database
    #     booking = Booking(
    #         pickup_location=pickup_location,
    #         pickup_date=pickup_date,
    #         pickup_time=pickup_time,
    #         dropoff_location=dropoff_location,
    #         dropoff_date=dropoff_date,
    #         dropoff_time=dropoff_time
    #     )
    #     booking.save()
    #     return redirect(available_car)

    # return render(req, 'user/user.html')
    if req.method == 'POST':
        # Access form data directly from req.POST
        pickup_location = req.POST.get('pickup-location')
        pickup_date = req.POST.get('pickup-date')
        pickup_hour = req.POST.get('pickup-hour')
        pickup_minute = req.POST.get('pickup-minute')
        pickup_ampm = req.POST.get('pickup-ampm')
        
        dropoff_location = req.POST.get('dropoff-location')
        dropoff_date = req.POST.get('dropoff-date')
        dropoff_hour = req.POST.get('dropoff-hour')
        dropoff_minute = req.POST.get('dropoff-minute')
        dropoff_ampm = req.POST.get('dropoff-ampm')

        # Combine the hour, minute, and AM/PM into a full time string (24-hour format)
        pickup_time_str = f"{pickup_hour}:{pickup_minute} {pickup_ampm}"
        dropoff_time_str = f"{dropoff_hour}:{dropoff_minute} {dropoff_ampm}"

        # Convert time to 24-hour format for storing in the database
        pickup_time = datetime.strptime(pickup_time_str, "%I:%M %p").time()
        dropoff_time = datetime.strptime(dropoff_time_str, "%I:%M %p").time()

        # Convert dates from string to date objects
        pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()
        dropoff_date = datetime.strptime(dropoff_date, "%Y-%m-%d").date()

        # Save the booking to the database
        booking = Booking(
            pickup_location=pickup_location,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            dropoff_location=dropoff_location,
            dropoff_date=dropoff_date,
            dropoff_time=dropoff_time,
            user=req.user  # Assuming the user is logged in
        )
        
        try:
            booking.save()
            return redirect('available_car', booking_id=booking.id)  # Redirect to available_car with booking ID
        except Exception as e:
            # Handle the error (e.g., log it, show a message, etc.)
            print(f"Error saving booking: {e}")
            # Optionally, you can redirect to an error page or show a message

    return render(req, 'user/user.html')
 
def available_car(req, booking_id):
    # Retrieve the booking using the provided booking_id
    booking = get_object_or_404(Booking, pk=booking_id)

    # Get the pickup and dropoff dates and times from the booking
    pickupdate = booking.pickup_date
    dropoff_date = booking.dropoff_date
    pickup_time = booking.pickup_time
    dropoff_time = booking.dropoff_time

    # Calculate the difference between pickup and dropoff dates
    delta_days = (dropoff_date - pickupdate).days  # Get the number of full days

    # Calculate total hours and minutes
    pickup_datetime = datetime.combine(pickupdate, pickup_time)
    dropoff_datetime = datetime.combine(dropoff_date, dropoff_time)
    total_duration = dropoff_datetime - pickup_datetime

    total_hours = total_duration.seconds // 3600  # Total hours
    total_minutes = (total_duration.seconds // 60) % 60  # Remaining minutes

    # Fetch available cars
    available_cars = Cars.objects.all()  # Modify this to filter based on your criteria

    # Calculate total cost for each car based on the number of days and price per day
    total_costs = []
    for car in available_cars:
        total_cost = (car.price_per_day * delta_days) + (car.price_per_day / 24 * total_hours) + (car.price_per_day / 1440 * total_minutes)
        total_costs.append({
            'car': car,
            'total_cost': total_cost
        })

    return render(req, 'user/available-cars.html', {
        'data': total_costs,
        'total_days': delta_days,
        'total_hours': total_hours,
        'total_minutes': total_minutes
    })


# def view_cars(req,cid):
#     if 'user' in req.session:
#         data=Cars.objects.get(pk=cid)
#         return render(req,'user/viewcars.html',{'data':data})
#     else:
#          return redirect(car_login)


