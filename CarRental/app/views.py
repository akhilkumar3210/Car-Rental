from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import Http404
from datetime import datetime
from django.http import HttpResponse
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
        
def delete_make(req,id):
     data=Makes.objects.get(pk=id)
     data.delete()
     return redirect(makess)

def view_make(req,id):
    make= Makes.objects.get(pk=id)
    cars = Cars.objects.filter(make=make)
    return render(req, 'shop/view_make.html', {'make': make,'cars': cars})

def delete_cars(req,pid):
    data=Cars.objects.get(pk=pid)
    file=data.image.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

def edit_cars(req,id):
    if req.method=='POST':
        model=req.POST['model']
        year=req.POST['year']
        body_type=req.POST['body_type']
        fuel=req.POST['fuel']
        transmission=req.POST['transmission']
        mileage=req.POST['mileage']
        price_per_day=req.POST['price_per_day']
        description=req.POST['description']
        image=req.FILES.get('image')
        if image:
            Cars.objects.filter(pk=id).update(model= model,year=year,bodytype=body_type, fuel= fuel,transmission=transmission, mileage= mileage,price_per_day=price_per_day,description=description)
            data=Cars.objects.get(pk=id)
            data.image=image
            data.save()
        else:
            Cars.objects.filter(pk=id).update(model= model,year=year,bodytype=body_type, fuel= fuel,transmission=transmission, mileage= mileage,price_per_day=price_per_day,description=description)
        return redirect(shop_home)
    else:
        car=Cars.objects.get(pk=id)      
        return render(req,'shop/edit.html',{'car':car})
# ___________________________________________________________________________ADMIN_________________________________________________________________________________________
def user_home(req):
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

def view_makes(req,id):
    if 'user' in req.session:
        make= Makes.objects.get(pk=id)
        cars = Cars.objects.filter(make=make)
        cat=Makes.objects.all()
        return render(req,'user/viewmake.html', {'make': make,'cars': cars,'cat':cat})
    else:
         return redirect(car_login)
 
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
    
    data1=Makes.objects.all()
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
        'total_minutes': total_minutes,
        'booking': booking,  
        'data1':data1
    })


def BookNow(req, cid, total_cost):
    if 'user' in req.session:
            car = get_object_or_404(Cars, pk=cid)
            user = get_object_or_404(User, username=req.session['user'])
            total_cost = float(total_cost)
            booking = Booking.objects.filter(user=user).first()

            if req.method == "POST":
                name = req.POST.get('name')
                email = req.POST.get('email')
                phone_number = req.POST.get('phone_number')
                date_of_birth = req.POST.get('date_of_birth')
                driving_license_front = req.FILES.get('driving_license_front')
                driving_license_back = req.FILES.get('driving_license_back')

                if not driving_license_front or not driving_license_back:
                    return HttpResponse("Both front and back sides of the driving license are required.", status=400)

                allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf']

                def is_valid_file(file):
                    return file.name.split('.')[-1].lower() in allowed_extensions

                if not is_valid_file(driving_license_front) or not is_valid_file(driving_license_back):
                    return HttpResponse("Invalid file format. Allowed formats: jpg, jpeg, png, pdf.", status=400)

                # Check if a profile already exists for the user
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': name,
                        'email': email,
                        'phone_number': phone_number,
                        'date_of_birth': date_of_birth,
                        'driving_license_front': driving_license_front,
                        'driving_license_back': driving_license_back,
                    }
                )

                if not created:
                    # If the profile already exists, update the existing profile
                    profile.name = name
                    profile.email = email
                    profile.phone_number = phone_number
                    profile.date_of_birth = date_of_birth
                    profile.driving_license_front = driving_license_front
                    profile.driving_license_back = driving_license_back
                    profile.save()

                # Create a Buy instance
                buy = Buy.objects.create(
                    booking=booking,
                    car=car,
                    user=user,
                    profile=profile,
                    tot_price=total_cost
                )

                return redirect('checkout', cid=car.id, booking_id=booking.id)

            return render(req, 'user/profile.html', {'car': car, 'total_cost': total_cost, 'booking': booking})
    else:
         return redirect(car_login)
    


def checkout(req, cid, booking_id):
    # Retrieve the specific booking
    booking = get_object_or_404(Booking, pk=booking_id)
    car = get_object_or_404(Cars, pk=cid)  # Using primary key (pk)
    user = booking.user

    # Retrieve the user's profile
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        messages.error(req, "Profile does not exist. Please complete your profile.")
        return redirect('profile_edit')  # Ensure this matches your actual profile edit URL name

    # Calculate the total cost
    total_cost = calculate_total_cost(car, booking)

    if req.method == 'POST':
        co_driver_added = req.POST.get('co_driver') == "on"  # Checkbox handling
        if co_driver_added:
            total_cost += 800  # Add co-driver fee
            messages.info(req, "Co-driver added. Total cost updated.")

    # Booking details (reversed order)
    booking_details = [
        ('Pickup Location', booking.pickup_location),
        ('Pickup Date', booking.pickup_date),
        ('Pickup Time', booking.pickup_time),
        ('Dropoff Location', booking.dropoff_location),
        ('Dropoff Date', booking.dropoff_date),
        ('Dropoff Time', booking.dropoff_time),
    ][::-1]  

    return render(req, 'user/checkout.html', {
        'booking_details': booking_details,
        'car': car,
        'profile': profile,
        'total_cost': total_cost,
    })



def calculate_total_cost(car, booking):
    price_per_day = car.price_per_day
    rental_duration = (booking.dropoff_date - booking.pickup_date).days
    return price_per_day * rental_duration


# def buyNow(req,pid):
#     if 'user' in req.session:
#         prod=Details.objects.get(pk=pid)
#         user=User.objects.get(username=req.session['user'])
#         data=Address.objects.filter(user=user)
#         if data:
#             return redirect("orderSummary",prod=prod.pk,data=data)
#         else:
#             if req.method=='POST':
#                 user=User.objects.get(username=req.session['user'])
#                 name=req.POST['name']
#                 address=req.POST['address']
#                 street=req.POST['street']
#                 city=req.POST['city']
#                 state=req.POST['state']
#                 pin=req.POST['pin']
#                 phone=req.POST['phone']
#                 data=Address.objects.create(user=user,name=name,address=address,street=street,city=city,state=state,pincode=pin,phone=phone)
#                 data.save()
#                 return redirect("orderSummary",prod=prod.pk,data=data)
#             else:
#                 return render(req,"user/address.html")
#     else:
#                 return redirect(car_login) 

def profile_success(req):
    return HttpResponse("Profile saved successfully!")
# def checkout(req):
     
#      return render(req,'user/checkout.html')

# def view_cars(req,cid):
#     if 'user' in req.session:
#         data=Cars.objects.get(pk=cid)
#         return render(req,'user/viewcars.html',{'data':data})
#     else:
#          return redirect(car_login)


