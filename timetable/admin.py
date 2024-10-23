from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, Staff, Subject, Timetable

admin.site.register(Course)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Timetable)

