# payment/urls.py
from django.urls import path
from .views import pay_bill

urlpatterns = [
    path('api/v1/pay-bill', pay_bill, name='pay_bill'), 
]