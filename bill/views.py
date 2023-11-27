# views.py
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Bill
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import BillSerializer


def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="bill_payment_history.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def bill_payment_history(request):
    bills = Bill.objects.all()
    context = {'bills': bills}
    return render_to_pdf('bill_payment_history.html', context)

def generate_report(request):
    # Your logic for generating the report goes here
    return render(request, 'admin/generate_report.html')  

@api_view(['POST'])
def pay_bill(request):
    try:
        # Deserialize the JSON payload using the serializer
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            # Access validated data through serializer.validated_data
            validated_data = serializer.validated_data

            # Separate validation for each field
            bill_type = validated_data.get('bill_type')
            amount = validated_data.get('amount')
            customer_id = validated_data.get('customer_id')

            if not bill_type:
                return JsonResponse({'error': 'Bill type is required.'}, status=400)

            if not amount:
                return JsonResponse({'error': 'Amount is required.'}, status=400)

            if not customer_id:
                return JsonResponse({'error': 'Customer Id is required.'}, status=400)

            # Optional field
            remark = validated_data.get('remark', '')

            # Perform payment process here.

            # If the payment process is successful, return success message
            response_data = {'message': 'Payment is successful'}
            return JsonResponse(response_data)
        else:
            # If validation fails, return the validation errors
            return JsonResponse({'error': serializer.errors}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in the request.'}, status=400)
