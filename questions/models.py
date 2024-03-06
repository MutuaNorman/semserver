from django.db import models
from accounts.models import CustomUser

class Year(models.Model):
    year_number = models.PositiveIntegerField()
        
    def __str__(self):
        return f"Year {self.year_number}"    


class Unit(models.Model):
    SPECIALIZATION_CHOICES = [
        ("B", 'Bcom'),
        ("P", 'Procurement'),
        ("E", 'Entrepreneurship'),
        ("A", 'All')
    ]

    GROUP_CHOICES = [
        ("A", 'Accounting'),
        ("F", 'Finance'),
        ("IS", 'Information Systems'),
        ("I", 'Insurance'),
        ("H", 'Human Resource'),
        ("M", 'Marketing'),
        ("C", 'Common Unit')
    ]

    unit_code = models.CharField(max_length=255)
    unit_description = models.CharField(max_length=255)
    unit_year = models.ForeignKey(Year, on_delete=models.CASCADE)
    unit_specialization = models.CharField(choices=SPECIALIZATION_CHOICES, default="A")
    group = models.CharField(choices=GROUP_CHOICES, default="A")

    def __str__(self):
        return self.unit_code


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ("E", "Exam"),
        ("C", "Cat")
    ]
    question_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_marks = models.PositiveIntegerField(null=True)
    question_image = models.ImageField(upload_to="question_images", blank=True, null=True)
    question_answer = models.TextField(null=True, blank=True)
    question_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    question_type = models.CharField(choices=QUESTION_TYPE_CHOICES, default="E")
    question_year = models.ForeignKey(Year, on_delete=models.CASCADE)
    question_academic_year = models.PositiveIntegerField(null=True)
    question_views = models.PositiveIntegerField(default=0)
    question_up_votes = models.PositiveIntegerField(default=0)
    question_down_votes = models.PositiveIntegerField(default=0)
    question_created_at = models.DateTimeField(auto_now_add=True)
    question_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text
