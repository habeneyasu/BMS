from django.shortcuts import render, redirect
from .forms import BillTypeForm
# Create your views here.

def create_bill_type(request):
    if request.method == 'POST':
        form = BillTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = BillTypeForm()

    return render(request, 'create_bill_type.html', {'form': form})