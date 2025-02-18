from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
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
        return render(req,'shop/shop.html')

def addcars(req):
        if 'shop' in req.session:
                if req.method=='POST':
                        cid=req.POST['cid']
                        model=req.POST['model']
                        year=req.POST['year']
                        color=req.POST['color']
                        license_plate=req.POST['license_plate']
                        mileage=req.POST['mileage']
                        price_per_day=req.POST['price_per_day']
                        description=req.POST['description']
                        is_available=req.POST['is_available']
                        image=req.FILES['image']
                        data=Cars.objects.create( cid=cid,model=model, year=year,color=color, license_plate=license_plate,mileage=mileage, price_per_day= price_per_day,description=description, is_available=is_available,image=image)
                        data.save()
                else:
                        # data=Category.objects.all()       
                        return render(req,'shop/addcars.html')
        else:
                return redirect(car_login)

def user_home(req):
        return render(req,'user/user.html')

