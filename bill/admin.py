from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils import timezone
from .models import Bill
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect


class BillAdminForm(forms.ModelForm):
    class Meta:
        model = Bill
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by', 'paid_date']
    def __init__(self, *args, **kwargs):
        super(BillAdminForm, self).__init__(*args, **kwargs)

        # Exclude 'Admin' and 'Biller' from the customer dropdown
        self.fields['customer_id'].queryset = User.objects.exclude(username__in=['Admin', 'Biller'])

class BillAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'custom_bill_type', 'amount', 'formatted_due_date', 'custom_created_by', 'remark', 'custom_status')
    search_fields = ['bill_type__name', 'amount', 'due_date', 'created_by__username', 'remark']  # Add fields you want to search here

    form = BillAdminForm

    actions = ['mark_as_paid','generate_pdf_action']

    def generate_pdf_action(self, request, queryset):
        # Get the URL for the generate_pdf_report view
        url = reverse('generate_pdf')

        # Redirect to the generate_pdf_report view for all bills
        return redirect(f"{url}")

    generate_pdf_action.short_description = 'Generate report'

    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new object (creation)
            obj.created_by = request.user
            obj.created_at = timezone.now()
        else:  # If it's an update
            obj.updated_by = request.user
            obj.updated_at = timezone.now()

        super().save_model(request, obj, form, change)

    def custom_bill_type(self, obj):
        return obj.bill_type.name if obj.bill_type else ''

    custom_bill_type.short_description = 'Bill Type'

    def custom_created_by(self, obj):
        # Check if the user has both first_name and middle_name
        if obj.created_by.first_name and obj.created_by.last_name:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        elif obj.created_by.first_name:
            return obj.created_by.first_name
        else:
            return obj.created_by.username

    custom_created_by.short_description = 'Created By'

    def customer_name(self, obj):
        # Check if the user has both first_name and middle_name
        if obj.customer_id.first_name and obj.customer_id.last_name:
            return f"{obj.customer_id.first_name} {obj.customer_id.last_name}"
        elif obj.creacustomer_idted_by.first_name:
            return obj.customer_id.first_name
        else:
            return obj.createcustomer_idd_by.username

    customer_name.short_description = 'Customer Name'

    def formatted_due_date(self, obj):
        # Check if due_date is not None before formatting
        if obj.due_date:
            return obj.due_date.strftime('%d-%m-%Y')
        else:
            return None

    formatted_due_date.short_description = 'Due Date'

    def custom_status(self, obj):
        # Calculate the status based on existing fields (due date, paid date)
        current_date = timezone.now().date()

        # Extract date, month, and year components for comparison
        due_date_components = (obj.due_date.day, obj.due_date.month, obj.due_date.year)
        current_date_components = (current_date.day, current_date.month, current_date.year)

        if due_date_components > current_date_components and not obj.paid_date:
            return format_html(
                '<div class="btn-group btn-group-toggle">'
                '<button type="button" style="margin-right: 2px;background-color: yellow; color: black;">Pending</button>'
                '</div>', obj.id
            )
        elif due_date_components < current_date_components and not obj.paid_date:
            return format_html(
                '<div class="btn-group btn-group-toggle">'
                '<button type="button" style="margin-right: 2px;background-color: red; color: black;">Overdue</button>'
                '</div>', obj.id
            )
        elif due_date_components == current_date_components and not obj.paid_date:
              return format_html(
                '<div class="btn-group btn-group-toggle">'
                '<button type="button" style="margin-right: 2px;background-color: green; color: black;" disabled>Paid</button>'
                '</div>'
            )
        else:
            return format_html(
                '<div class="btn-group btn-group-toggle">'
                '<button type="button" style="margin-right: 2px;background-color: green; color: black;" disabled>Paid</button>'
                '</div>'
            )

    custom_status.short_description = 'Status'

    def get_queryset(self, request):
        # If the user is "Admin" or "Biller", show all bills
        if request.user.username in ['Admin', 'Biller']:
            return super().get_queryset(request)

        # If it's another user, filter bills based on the logged-in user's ID
        return super().get_queryset(request).filter(customer_id=request.user.id)

  

    def mark_as_paid(self, request, queryset):
        # Action to mark selected bills as paid
        queryset.update(paid_date=timezone.now())
        self.message_user(request, f'Bill paid successfully.')

    mark_as_paid.short_description = 'Mark bills to pay'

  


# Register the model with the custom admin class
admin.site.register(Bill, BillAdmin)
