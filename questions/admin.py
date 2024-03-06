from django.contrib import admin
from .models import *

class YearModelAdmin(admin.ModelAdmin):
    list_display = ["id", "year_number"]

class UnitModelAdmin(admin.ModelAdmin):
    list_display = ["id", "unit_code", "unit_description", "unit_year"]

admin.site.register(Year, YearModelAdmin)

admin.site.register(Unit, UnitModelAdmin)

admin.site.register(Question)






