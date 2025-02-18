from django.urls import path
from . import views
urlpatterns=[
     path('',views.car_login),
     path('register',views.register),
     path('logout',views.car_logout),
     path('shop_home',views.shop_home),
     path('addcars',views.addcars),

     path('user_home',views.user_home),





    
]