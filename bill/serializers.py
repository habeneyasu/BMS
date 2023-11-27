# serializers.py in your app
from rest_framework import serializers

class BillSerializer(serializers.Serializer):
    bill_type = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    customer_id = serializers.IntegerField(required=True)
    remark = serializers.CharField(required=False, allow_blank=True)
