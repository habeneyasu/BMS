from django.db import models
from bill.models import Bill
from django.contrib.auth.admin import User
# Create your models here.
class Payment(models.Model):
    id=models.AutoField(primary_key=True)
    bill_name=models.ForeignKey(Bill,on_delete=models.CASCADE, null=False)
    amount=models.FloatField()
    payment_choices = (
        ('Credit card', 'credit card'),
        ('Bank transfer', 'bank transfer'),
    )
    payment_method = models.CharField(max_length=15, choices=payment_choices)
    payment_date=models.DateField(auto_now_add=True,null=True)
    updated_at=models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_payments')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='updated_payments')
    

    def __str__(self):
        return f"{self.bill_name.bill_type.name}"
    
# payment/serializers.py
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
     class Meta:
        model = Payment
        fields = '__all__'