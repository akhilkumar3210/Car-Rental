from django.urls import path
from . import views
urlpatterns=[
     path('',views.car_login),
     path('register',views.register),
     path('logout',views.car_logout),
     path('shop_home',views.shop_home),
     path('addcars',views.addcars),
     path('makes',views.makess),


     path('user_home', views.user_home),
     path('available-cars/<booking_id>', views.available_car, name='available_car'),
     path('BookNow/<cid>/<total_cost>', views.BookNow, name='BookNow'),
     path('profile_success', views.profile_success),
     path('checkout/<cid>/<booking_id>', views.checkout, name='checkout'),




    
]