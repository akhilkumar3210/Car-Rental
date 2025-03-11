from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import Http404
import json
from datetime import datetime
import math,random
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
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
        name=req.POST['uname']
        password=req.POST['password']
        otp=OTP(req)
        if User.objects.filter(email=email).exists():
            messages.error(req, "Email is already in use.")
            return redirect(register)
        else:
            send_mail('Your registration OTP ,',f"OTP for registration is {otp}", settings.EMAIL_HOST_USER, [email])
            messages.success(req, "Registration successful. Please check your email for OTP.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
        # try:
        #     data=User.objects.create_user(first_name=uname,email=email,username=email,password=password)
        #     data.save()
        # #     send_mail('Registration In EcommShop', 'Successfully Registered In EcommShop', settings.EMAIL_HOST_USER, [email])
        #     return redirect(car_login)
        # except:
        #     messages.warning(req,'Email Already Exists!!')
        #     return redirect(register)
    else:
        return render(req,'register.html')
    
def OTP(req):
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def validate(req,name,password,email,otp):
    if req.method=='POST':
        uotp=req.POST['uotp']
        if uotp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req, "OTP verified successfully. You can now log in.")
            return redirect(car_login)
        else:
            messages.error(req, "Invalid OTP. Please try again.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'validate.html',{'name':name,'pass':password,'email':email,'otp':otp})


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
        is_available = req.POST.get('is_available') == 'on' 

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
                image=image,
                is_available=is_available
            )
            return redirect(shop_home)

        except ValidationError as e:
            error_message = e.message
            return render(req, 'shop/addcars.html', {'error_message': error_message, 'data': data})

    else:
        data = Makes.objects.all()
        return render(req, 'shop/addcars.html', {'data': data})
    
def locations(req):
    if 'shop' in req.session:
                if req.method == 'POST':
                        location=req.POST['location']
                        data=Location.objects.create(location=location)
                        data.save()
                        return redirect(locations)
                else:
                        data=Location.objects.all()
                        return render(req,'shop/location.html',{'data':data})
    else:
             redirect(car_login)

def delete_locations(req,id):
     data=Location.objects.get(pk=id)
     data.delete()
     return redirect(locations)
    
def customerprofile(req):
     data=Profile.objects.all()
     return render(req,'shop/profile.html',{'data':data})

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
        is_available = req.POST.get('is_available') == 'on' 
        if image:
            Cars.objects.filter(pk=id).update(model= model,year=year,bodytype=body_type, fuel= fuel,transmission=transmission, mileage= mileage,price_per_day=price_per_day,description=description,is_available= is_available)
            data=Cars.objects.get(pk=id)
            data.image=image
            data.save()
        else:
            Cars.objects.filter(pk=id).update(model= model,year=year,bodytype=body_type, fuel= fuel,transmission=transmission, mileage= mileage,price_per_day=price_per_day,description=description,is_available= is_available)
        return redirect(shop_home)
    else:
        car=Cars.objects.get(pk=id)      
        return render(req,'shop/edit.html',{'car':car})
    
def rentedcars(req):
     rented = Rented.objects.all()
     return render(req,'shop/rentedcars.html',{'data':rented})
# ___________________________________________________________________________ADMIN_________________________________________________________________________________________

def user_home(req):
    if 'user' in req.session:
        if req.method == 'POST':
            # Check if the user is selecting a new booking option
            if 'clear_booking' in req.POST:
                # Clear existing booking data from the session
                req.session['pickup_location'] = None
                req.session['pickup_date'] = None
                req.session['pickup_time'] = None
                req.session['dropoff_location'] = None
                req.session['dropoff_date'] = None
                req.session['dropoff_time'] = None
                messages.info(req, "Existing booking data cleared.")
                return redirect('user_home')  # Redirect to the same page to refresh the form

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

            # Validate that pickup date is before dropoff date
            if pickup_date > dropoff_date:
                messages.error(req, "Pickup date cannot be after drop-off date.")
                return render(req, 'user/user.html')

            # Automatically delete existing bookings for the user
            Booking.objects.filter(user=req.user).delete()

            # Save the new booking to the database
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
                messages.success(req, "Booking created successfully!")
                return redirect('available_car', booking_id=booking.id)  # Redirect to available_car with booking ID
            except Exception as e:
                messages.error(req, f"Error saving booking: {e}")
                return render(req, 'user/user.html')

        data=Location.objects.all()
        return render(req, 'user/user.html',{'data':data})
    else:
        return redirect(car_login)
    
def view_makes(req,id):
    if 'user' in req.session:
        make= Makes.objects.get(pk=id)
        cars = Cars.objects.filter(make=make)
        cat=Makes.objects.all()
        return render(req,'user/viewmake.html', {'make': make,'cars': cars,'cat':cat})
    else:
         return redirect(car_login)
 
def available_car(req, booking_id):
    if 'user' in req.session:
                booking = get_object_or_404(Booking, pk=booking_id)
                pickupdate = booking.pickup_date
                dropoff_date = booking.dropoff_date
                pickup_time = booking.pickup_time
                dropoff_time = booking.dropoff_time

                delta_days = (dropoff_date - pickupdate).days
                pickup_datetime = datetime.combine(pickupdate, pickup_time)
                dropoff_datetime = datetime.combine(dropoff_date, dropoff_time)
                total_duration = dropoff_datetime - pickup_datetime

                total_hours = total_duration.seconds // 3600
                total_minutes = (total_duration.seconds // 60) % 60

                available_cars = Cars.objects.all()
                data1 = Makes.objects.all()
                
                total_costs = []
                for car in available_cars:
                    total_cost = (car.price_per_day * delta_days) + (car.price_per_day / 24 * total_hours) + (car.price_per_day / 1440 * total_minutes)
                    total_cost = round(total_cost)
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
                    'data1': data1
                })
    else:
         return redirect(car_login)
    
def addprofile(req):
    if 'user' in req.session:
            user = get_object_or_404(User, username=req.session['user'])
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

                        profile = Profile.objects.create(
                            user=user,
                            name=name,
                            email=email,
                            phone_number=phone_number,
                            date_of_birth=date_of_birth,
                            driving_license_front=driving_license_front,
                            driving_license_back=driving_license_back
                        )


                        return redirect(user_home)

            return render(req,'user/addprofile.html')
    else:
         return redirect(car_login)


def BookNow(req, cid, total_cost):
    if 'user' in req.session:
        car = get_object_or_404(Cars, pk=cid)
        user = get_object_or_404(User, username=req.session['user'])
        total_cost = float(total_cost)
        booking = Booking.objects.filter(user=user).first() 
        profile = Profile.objects.filter(user=user).first()  # Get the first profile or None

        if profile:
            buy = Buy.objects.create(
                booking=booking,
                car=car,
                user=user,
                profile=profile,
                tot_price=total_cost
            )
            return redirect('checkout', cid=car.id, booking_id=booking.id, buy_id=buy.id)
        else:
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

                profile = Profile.objects.create(
                    user=user,
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    date_of_birth=date_of_birth,
                    driving_license_front=driving_license_front,
                    driving_license_back=driving_license_back
                )

                buy = Buy.objects.create(
                    booking=booking,
                    car=car,
                    user=user,
                    profile=profile,
                    tot_price=total_cost
                )

                return redirect('checkout', cid=car.id, booking_id=booking.id, buy_id=buy.id)

            return render(req, 'user/profile.html', {'car': car, 'total_cost': total_cost, 'booking': booking})
    else:
        return redirect(car_login)


def checkout(req, cid, booking_id, buy_id):
    user = req.user  # Get the currently logged-in user

    # Ensure the user is authenticated
    if not user.is_authenticated:
        messages.error(req, "You need to be logged in to access this page.")
        return redirect('login')  # Redirect to login page if not authenticated

    # Get the booking for the user
    booking = get_object_or_404(Booking, pk=booking_id, user=user)
    car = get_object_or_404(Cars, pk=cid)
    buy = get_object_or_404(Buy, pk=buy_id)
    req.session['cars']=car.pk
    

    # Retrieve the user's profile
    profile = Profile.objects.filter(user=user).first()
    if not profile:
        messages.error(req, "Profile does not exist. Please complete your profile.")
        return redirect('profile_edit')

    # Define co-driver fee
    co_driver_fee = 500

    # Initialize total costs
    total_without_co_driver = buy.tot_price
    total_with_co_driver = total_without_co_driver + co_driver_fee

    if req.method == 'POST':
        # Check if the co-driver option is selected
        co_driver_added = req.POST.get('co_driver') == "on"
        
        # Calculate total cost based on co-driver selection
        if co_driver_added:
            total_cost = total_with_co_driver
            messages.info(req, "Co-driver added. Total cost updated to ₹{:.2f}".format(total_cost))
        else:
            total_cost = total_without_co_driver
            messages.info(req, "Co-driver option not selected. Total cost remains at ₹{:.2f}".format(total_cost))

        if car.is_available:
            rented = Rented.objects.create( buy=buy,
            booking=booking,
            car=car,
            user=user,
            profile=profile,
            tot_price=total_cost)
            rented.save()
            # Set car as not available
            car.is_available = False
            car.save()
        # Redirect to the rent_payment view with the total amount
        return redirect('rent_payment', total_amount=total_cost)  # Redirect to rent_payment view

   
    return render(req, 'user/checkout.html', {
        'booking': booking,
        'car': car,
        'profile': profile,
        'total_without_co_driver': total_without_co_driver,
        'total_with_co_driver': total_with_co_driver,
        'buy': buy
    })

def profile_success(request):
    return render(request, 'user/profile_success.html')


def rent_payment(req, total_amount):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        name = user.first_name
        amount = int(float(total_amount)) 
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(car_login)
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})  
 
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            
        return redirect("rentbook")

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  
    

def rentbook(req):
    if 'user' in req.session:
        try:
            user = User.objects.get(username=req.session['user'])
            rented = Rented.objects.filter(user=user)  # Filter rented cars by the current user
            return render(req, 'user/rentbook.html', {'data': rented})
        except ObjectDoesNotExist:
            # Handle the case where the user or car does not exist
            return render(req, 'user/rentbook.html', {'error': 'User  or car not found.'})
    else:
        return redirect(car_login)
    
