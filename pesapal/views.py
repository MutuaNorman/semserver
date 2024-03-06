from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse
from decouple import config
import uuid
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import CustomUser
from .serializers import PaymentSerializer
from .models import Payment
from questions.permissions import IsSuperuserOrReadOnly

class GetPaymentsApiView(APIView):
    permission_classes = [IsSuperuserOrReadOnly]

    def get(self, request):
        payments =  Payment.objects.all() 
        serializer = PaymentSerializer(payments, many=True)
        response = {
            "message": "Success",
            "data" : serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)

def get_pesapal_token(request):
    consumer_key = config("PESAPAL_CONSUMER_KEY")
    consumer_secret = config("PESAPAL_CONSUMER_SECRET")

    pesapal_token_url = config("PESAPAL_TOKEN_URL")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    data = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret,
    }

    try:
        response = requests.post(pesapal_token_url, json=data, headers=headers)

        if response.status_code == 200:
            return response
        else:
            return JsonResponse(
                {"error": f'Request failed with status code {response.status_code}'},
                status=500,
            )

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_pesapal_IPN(request):
    pesapal_ipn_url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"

    try:
        token_response = get_pesapal_token(request)
        token_data = token_response.json()
        token = token_data.get("token")

        bearer_token = f"Bearer {token}"

        headers = {
            "Authorization": bearer_token,
        }

        data = {
            "url": "http://localhost:8000/ipn",
            "ipn_notification_type": "GET",
        }

        response = requests.post(pesapal_ipn_url, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            ipn_id = response_data.get("ipn_id")
            return JsonResponse({"ipn_id": ipn_id})
        else:
            return JsonResponse(
                {"error": f"Request failed with status code {response.status_code}"},
                status=500,
            )

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def register_pesapal_ipn(request):
    pesapal_register_url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"

    try:
        token_response = get_pesapal_token(request)
        token_data = token_response.json()
        token = token_data.get("token")

        bearer_token = f"Bearer {token}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": bearer_token,
        }

        data = {
            "url" : "http://localhost:8000/ipn",
            "ipn_notification_type": "GET"
        }

        response = requests.post(pesapal_register_url, json=data, headers=headers)     

        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse({"data": response_data})
        else:
            return JsonResponse(
                {"error": f"Request failed with status code {response.status_code}"},
                status=500,
            )

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def generate_merchant_reference(prefix="REF"):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4().hex)[:12]  # Using a portion of a UUID for uniqueness
    reference = f"{prefix}_{timestamp}_{unique_id}"
    return reference[:50]  

class pesapal_payAPIView(APIView):
    def post(self, request):
        data = request.data
        # return JsonResponse({"data":data}, status=200)

        try:
            token_response = get_pesapal_token(request)
            token_data = token_response.json()
            token = token_data.get("token")

            bearer_token = f"Bearer {token}"

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": bearer_token,
            }

            unique_reference = generate_merchant_reference()

                     
            order_data = {
                "id" : unique_reference,
                "currency": "KES",
                "amount": data['payData']['amount'],
                "description": f"Payment for a {data['payData']['duration']} plan",
                "callback_url": "https://sempolisher.com/dashboard/bcom",
                "redirect_mode": "",
                "notification_id": config("PESAPAL_IPN_ID"),
                "billing_address": {
                    "email_address": data["payData"]["customer_email"]
                }
            }

            pesapal_submit_order_url = config("PESAPAL_SUBMIT_ORDER_URL")

            response = requests.post(pesapal_submit_order_url, json=order_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                user_id = data['payData']["user_id"]
                user = get_object_or_404(CustomUser, id=user_id)
                user.has_paid = True
                user.payment_date = datetime.now()  
                user.payment_period = data['payData']['duration']
                # Calculate expiry_date based on payment_period
                if user.payment_period == 'monthly':
                    user.expiry_date = user.payment_date + timedelta(days=30)
                elif user.payment_period == 'semester':
                    user.expiry_date = user.payment_date + timedelta(days=180)
                elif user.payment_period == 'yearly':
                    user.expiry_date = user.payment_date + timedelta(days=365)  
                user.save()
                return JsonResponse({"data": response_data})
            else:
                return JsonResponse(
                    {"error": f"Request failed with status code {response.status_code}"},
                    status=500,
                )

        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
        
      
