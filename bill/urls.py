from django.urls import path
from .views import pay_bill,generate_pdf


urlpatterns = [
   
    path('api/v1/pay-bill', pay_bill, name='pay_bill'),
    path('generate_pdf', generate_pdf, name='generate_pdf'),
   ]

