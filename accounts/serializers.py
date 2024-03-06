from djoser.serializers import UserCreateSerializer
from .models import CustomUser


class CustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ["id", "email", "name", "password", "has_paid", "payment_date", "payment_period"]
          

