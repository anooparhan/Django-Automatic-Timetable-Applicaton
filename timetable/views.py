import random
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Timetable, Subject, Staff
from .forms import TimetableForm
from django.db.models import Q
import random
from .forms import TimetableEditForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import CourseForm, StaffForm, SubjectForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('course_list') 
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')  


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})
def course_lists(request):
    courses = Course.objects.all()
    return render(request, 'course_lists.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form})



def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('course_list')


def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff_members': staff_members})

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'add_staff.html', {'form': form})

def edit_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff_member)
    return render(request, 'edit_staff.html', {'form': form})

def delete_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    staff_member.delete()
    return redirect('staff_list')


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})

def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'edit_subject.html', {'form': form})

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    return redirect('subject_list')


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(
        html, dest=result
    )
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return result

def download_timetable_pdf(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    timetable_entries = Timetable.objects.filter(course=course).order_by('day', 'time_slot')

    timetable = {day: [None] * 4 for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
    for entry in timetable_entries:
        timetable[entry.day][entry.time_slot - 1] = entry

    
    context = {
        'timetable': timetable,
        'course': course,
    }

    
    return render_to_pdf('timetable_pdf.html', context)


DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


def timetable_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    timetable_entries = Timetable.objects.filter(course=course).order_by('day', 'time_slot')

    
    timetable = {day: [None] * 4 for day in DAY_ORDER}

    for entry in timetable_entries:
        if entry.day in timetable:
            timetable[entry.day][entry.time_slot - 1] = entry

    if request.method == 'POST':
        form = TimetableForm(request.POST, course=course)
        if form.is_valid():
            form.save()
    else:
        form = TimetableForm(course=course)

    return render(request, 'timetable.html', {'timetable': timetable, 'course': course, 'form': form})




import random  

def generate_auto_timetable(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    subjects = list(Subject.objects.filter(course=course))  
    total_subjects = len(subjects)

    if total_subjects == 0:
        return redirect('timetable_view', course_id=course.id) 

   
    Timetable.objects.filter(course=course).delete()

    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [1, 2, 3, 4]

   
    random.shuffle(subjects)

    subject_index = 0  
    for day in days:
        available_staff = Staff.objects.all()  

        
        random.shuffle(subjects)

        for time_slot in time_slots:
           
            subject = subjects[subject_index % total_subjects]

            if subject.staff in available_staff:
          
                Timetable.objects.create(
                    course=course,
                    day=day,
                    time_slot=time_slot,
                    subject=subject
                )
              
                available_staff = available_staff.exclude(id=subject.staff.id)

         
            subject_index += 1

    return redirect('timetable_view', course_id=course.id)




def add_timetable_entry(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = TimetableForm(request.POST, course=course)
        if form.is_valid():
            form.save()
            return redirect('timetable_view', course_id=course.id)  
    else:
        form = TimetableForm(course=course)

    return render(request, 'add_timetable.html', {'form': form, 'course': course})



def edit_timetable_entry(request, entry_id):
    timetable_entry = get_object_or_404(Timetable, id=entry_id)
    
    if request.method == 'POST':
        form = TimetableEditForm(request.POST, instance=timetable_entry)
        if form.is_valid():
            form.save()
            return redirect('timetable_view', course_id=timetable_entry.course.id) 
    else:
        form = TimetableEditForm(instance=timetable_entry)

    return render(request, 'edit_timetable_entry.html', {'form': form, 'timetable_entry': timetable_entry})