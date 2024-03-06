from django.db import models
from django.utils import timezone

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as needed
    duration = models.CharField(max_length=20)  # Assuming duration can be 'monthly', 'semester', or 'yearly'
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)  # This field automatically updates when the object is saved

    def __str__(self):
        return f"Amount: Ksh. {self.amount} - Duration: {self.duration} - Created at: {self.created_at}"
