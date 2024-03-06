from django.urls import path
from . import views

urlpatterns = [
    path("years", views.GetYearsApiView.as_view()),
    path("years/<int:id>", views.GetUnitsApiView.as_view()),
    path("units/<int:id>/questions", views.GetQuestionsApiView.as_view()),
    path("question/<int:id>", views.GetQuestionDetailApiView.as_view())
]