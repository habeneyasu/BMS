from django.contrib import admin
from django.utils import timezone
from .models import Payment
from django import forms
from bill.models import Bill

class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['created_at','created_by','updated_at', 'updated_by']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('custom_bill_type', 'amount', 'payment_method', 'payment_date', 'custom_created_by')
    search_fields = ['bill_name__bill_type__name', 'amount', 'payment_method', 'payment_date', 'created_by__username']

    form = PaymentAdminForm

    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new object (creation)
            obj.created_by = request.user
        else:  # If it's an update
            obj.updated_by = request.user
            obj.updated_at = timezone.now()

        super().save_model(request, obj, form, change)

    def custom_bill_type(self, obj):
        return obj.bill_name.bill_type.name if obj.bill_name else ''

    custom_bill_type.short_description = 'Bill Type'

    def custom_created_by(self, obj):
        return obj.created_by.username if obj.created_by else ''

    custom_created_by.short_description = 'Created By'

# Register the model with the custom admin class
# admin.site.register(Payment, PaymentAdmin)
