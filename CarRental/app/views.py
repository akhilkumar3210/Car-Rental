from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
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
    if 'shop' in req.session:
        if req.method == 'POST':
            cid = req.POST['cid']
            model = req.POST['model']
            make = req.POST['p_makes']
            year = req.POST['year']
            color = req.POST['color']
            license_plate = req.POST['license_plate']
            mileage = req.POST['mileage']
            price_per_day = req.POST['price_per_day']
            description = req.POST['description']
            is_available = req.POST['is_available'] == 'on'
            image = req.FILES['image']

            if Cars.objects.filter(license_plate=license_plate).exists():
                messages.error(req, "This license plate already exists.")
                data = Makes.objects.all()
                return render(req, 'shop/addcars.html', {'data': data})

            try:
                data = Cars.objects.create(
                    cid=cid,
                    model=model,
                    make=Makes.objects.get(makes=make),
                    year=year,
                    color=color,
                    license_plate=license_plate,
                    mileage=mileage,
                    price_per_day=price_per_day,
                    description=description,
                    is_available=is_available,
                    image=image
                )
                data.save()
                messages.success(req, "Car added successfully!")
                return redirect(shop_home)
            except IntegrityError:
                messages.error(req, "An error occurred while adding the car. Please try again.")
                data = Makes.objects.all()
                return render(req, 'shop/addcars.html', {'data': data})

        else:
            data = Makes.objects.all()
            return render(req, 'shop/addcars.html', {'data': data})
    else:
        return redirect(car_login)

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
        data=Cars.objects.all() 
        return render(req,'user/user.html',{'data':data})


# def view_cars(req,cid):
#     if 'user' in req.session:
#         data=Cars.objects.get(pk=cid)
#         return render(req,'user/viewcars.html',{'data':data})
#     else:
#          return redirect(car_login)

def view_cars(req, cid):
    if 'user' in req.session:
        data = Cars.objects.get(pk=cid)
        
        total_price = 0
        start_date_str = ''
        end_date_str = ''
        
        # Check if the request method is POST to handle form submission
        if req.method == 'POST':
            start_date_str = req.POST.get('startDate')
            end_date_str = req.POST.get('endDate')
            
            # Convert string dates to datetime objects
            try:
                start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
                end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
                
                # Calculate the number of days
                delta = (end_date - start_date).days
                
                # Calculate total price
                if delta > 0:  # Ensure that the end date is after the start date
                    total_price = delta * data.price_per_day
                else:
                    total_price = 0  # Handle case where dates are invalid
            except ValueError:
                total_price = 0  # Handle case where date conversion fails

        return render(req, 'user/viewcars.html', {
            'data': data,
            'total_price': total_price,
            'start_date': start_date_str,
            'end_date': end_date_str
        })
    else:
        return redirect('car_login')  # Ensure you have the correct URL name for redirection