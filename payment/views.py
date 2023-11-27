from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import PaymentSerializer

@api_view(['POST'])
def pay_bill(request):
    try:
        # Deserialize the JSON payload using the serializer
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            # Access validated data through serializer.validated_data
            validated_data = serializer.validated_data

            # Separate validation for each field
            bill_type = validated_data.get('bill_type')
            amount = validated_data.get('amount')
            user_id = validated_data.get('user_id')

            if not bill_type:
                return JsonResponse({'error': 'Bill type is required.'}, status=400)

            if not amount:
                return JsonResponse({'error': 'Amount is required.'}, status=400)

            if not user_id:
                return JsonResponse({'error': 'User ID is required.'}, status=400)

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
