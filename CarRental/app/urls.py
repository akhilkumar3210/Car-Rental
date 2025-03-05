from django.urls import path
from . import views
urlpatterns=[
     path('',views.car_login),
     path('register',views.register),
     path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
     path('logout',views.car_logout),



     path('shop_home',views.shop_home),
     path('addcars',views.addcars),
     path('makes',views.makess),
     path('delete_make/<id>',views.delete_make),
     path('delete/<pid>',views.delete_cars),
     path('edit/<id>',views.edit_cars),
     path('view_make/<id>',views.view_make),
     path('customerprofile',views.customerprofile),



     path('user_home', views.user_home),
     path('view_makes/<id>',views.view_makes),
     path('available-cars/<booking_id>', views.available_car, name='available_car'),
     path('BookNow/<cid>/<total_cost>', views.BookNow, name='BookNow'),
     path('profile_success', views.profile_success),
     path('profile_success/', views.profile_success, name='profile_success'),
     path('checkout/<cid>/<booking_id>/<buy_id>', views.checkout, name='checkout'),
     path('rent_payment/<total_amount>',views.rent_payment,name="rent_payment"),
     path('callback',views.callback,name="callback"),
     path('rentbook',views.rentbook,name="rentbook")





    
]