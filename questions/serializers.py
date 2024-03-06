from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = "__all__"   

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"             