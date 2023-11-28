# views.py
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Bill
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import BillSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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


def generate_pdf(request):
    # Retrieve data from the database
    bills = Bill.objects.all()

    # Load the HTML template
    template_path = 'bill_report.html'
    context = {'bills': bills}
    template = get_template(template_path)
    html_content = template.render(context)

    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="bill_report.pdf"'

    # Create a PDF object using ReportLab
    pdf = pisa.CreatePDF(html_content, dest=response)

    # If PDF generation failed
    if pdf.err:
        return HttpResponse('Error during PDF generation: %s' % pdf.err)

    return response

def bill_status_reminder(request):
    return render(request, 'bill_status_reminder.html')
