from django import forms
from .models import Timetable, Subject
from .models import Course, Staff, Subject
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'available_days']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'course', 'staff']

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'day', 'time_slot', 'subject']

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        if course:
            self.fields['subject'].queryset = Subject.objects.filter(course=course)
class TimetableEditForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['subject'] 