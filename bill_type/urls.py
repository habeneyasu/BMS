from django.urls import path
from .views import create_bill_type  # Import your views

urlpatterns = [
    path('create-bill-type/', create_bill_type, name='create_bill_type'),
    # Add more paths for other views in your app
]