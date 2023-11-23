from django.urls import path
from . import views

urlpatterns=[
    path('success/',views.ReservationAPI,name="reservation"),
    path('',views.welcome,name='welcome')
    
    
]