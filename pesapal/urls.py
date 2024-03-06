from django.urls import path
from . import views

urlpatterns = [
    path("payments/", views.GetPaymentsApiView.as_view()),
    path("token/", views.get_pesapal_token),
    path("ipn/", views.get_pesapal_IPN),
    path("register/", views.register_pesapal_ipn),
    path("pay/",views.pesapal_payAPIView.as_view())
]