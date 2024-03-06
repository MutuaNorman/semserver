from django.urls import path
from .views import *

urlpatterns = [
    path("delete-user/<int:id>/", DeleteUserAPIView.as_view()),
]