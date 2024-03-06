from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

class DeleteUserAPIView(APIView):
    def delete(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.delete()
        return Response({'message': 'The account has been deleted'}, status=status.HTTP_200_OK)
        