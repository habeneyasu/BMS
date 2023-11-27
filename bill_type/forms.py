from django import forms
from .models import BillType

class BillTypeForm(forms.ModelForm):
    class Meta:
        model = BillType
        exclude = ['updated_at']

        fields = ['name', 'remark']  # Include only the fields you want to appear in the form

    def clean_name(self):
        name = self.cleaned_data['name']
        # Add any custom validation for the 'name' field if needed
        return name