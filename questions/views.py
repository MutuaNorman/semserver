from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from .permissions import IsSuperuserOrReadOnly
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsSuperuserOrReadOnly]


class GetYearsApiView(APIView):
    permission_classes = [IsSuperuserOrReadOnly] 

    def get(self, request):
        years =  Year.objects.all().order_by('year_number')  
        serializer = YearSerializer(years, many=True)
        response = {
            "message": "Success",
            "data" : serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)

class GetUnitsApiView(APIView):
    permission_classes = [IsSuperuserOrReadOnly] 

    def get(self, request, id):
        units = Unit.objects.filter(unit_year__year_number = id)
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetQuestionsApiView(APIView):
    permission_classes = [IsSuperuserOrReadOnly] 

    def get(self, request, id):
        unit = get_object_or_404(Unit, id=id) 
         
        questions = Question.objects.filter(unit=unit) 

        unit_serializer = UnitSerializer(unit)
        question_serializer = QuestionSerializer(questions, many=True)

        response = {
            "message": "Success",
            "data" : {
                "unit": unit_serializer.data,
                "questions" : question_serializer.data
            }
        }

        return Response(data=response, status=status.HTTP_200_OK)
    
class GetQuestionDetailApiView(APIView):
    permission_classes = [IsSuperuserOrReadOnly] 

    def get(self, request, id):
        question = get_object_or_404(Question, pk=id)

        serializer = QuestionSerializer(question)

        response = {
            "message": "Success",
            "data": serializer.data
        }

        return Response(data=response, status=status.HTTP_200_OK)
        