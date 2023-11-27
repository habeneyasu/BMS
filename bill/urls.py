from django.urls import path
from .views import bill_payment_history,pay_bill

urlpatterns = [
    path('bill-payment-history', bill_payment_history, name='bill_payment_history'),
    path('api/v1/pay-bill', pay_bill, name='pay_bill')
]

