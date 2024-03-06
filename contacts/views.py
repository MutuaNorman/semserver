from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import ContactSerializer

class ContactAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            # Customize the email message as needed
            email_message = f"From: {name} <{email}>\n\n{subject}\n\n{message}"
            
            # You might want to replace 'your_email@example.com' with your email address
            send_mail(subject, email_message, email, ['sempolisher@gmail.com'])
            
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)