from django.db import models
import json
from multiselectfield import MultiSelectField

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Staff(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    
    name = models.CharField(max_length=100)
    available_days = MultiSelectField(choices=DAY_CHOICES)  
    def __str__(self):
        return self.name


    def clean(self):
      
        try:
            json.dumps(self.available_days)  
        except (TypeError, ValueError):
            raise ValidationError("Available days must be a valid JSON array.")

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time_slot = models.IntegerField()  
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.name} - {self.day} - Period {self.time_slot}: {self.subject.name}"