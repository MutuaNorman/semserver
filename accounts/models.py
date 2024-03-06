from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    has_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    PAYMENT_PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('semester', 'Semester'),
        ('yearly', 'Yearly'),
    ]
    payment_period = models.CharField(max_length=10, choices=PAYMENT_PERIOD_CHOICES, null=True, blank=True)
    username = None
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "has_paid", "payment_date", "payment_period", "expiry_date"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


