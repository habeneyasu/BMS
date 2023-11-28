from django.db import models
from django.contrib.auth.models import User
from bill_type.models import BillType
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.
class Bill(models.Model):
    id=models.AutoField(primary_key=True)
    bill_type=models.ForeignKey(BillType,on_delete=models.CASCADE, null=False)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_name')
    amount=models.FloatField()
    due_date=models.DateTimeField(blank=False, null=False)
    created_at=models.DateField(auto_now_add=True,null=True)
    updated_at=models.DateField(blank=True, null=True)
    paid_date=models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_bills')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='updated_bills')
    remark=models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.bill_type.name}"
    
    # Bill/serializers.py
from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
     class Meta:
        model = Bill
        fields = '__all__'

@receiver(post_save, sender=Bill)
def send_update_to_websocket(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "bill_status_updates",
        {"type": "bill.update", "message": "Bill updated."},
    )

  

 