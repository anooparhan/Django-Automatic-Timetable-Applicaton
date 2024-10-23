from django.urls import path
from .views import course_list,timetable_view, generate_auto_timetable,register,user_login,user_logout
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('course_list', course_list, name='course_list'),
    path('timetable/<int:course_id>/', timetable_view, name='timetable_view'),
    path('course/<int:course_id>/add-timetable/', views.add_timetable_entry, name='add_timetable'),
    path('course/<int:course_id>/generate-timetable/', generate_auto_timetable, name='generate_auto_timetable'),
    path('edit-timetable-entry/<int:entry_id>/', views.edit_timetable_entry, name='edit_timetable_entry'),
    path('download-timetable-pdf/<int:course_id>/', views.download_timetable_pdf, name='download_timetable_pdf'),
    path('courses/', views.course_lists, name='course_lists'),
    path('courses/add/', views.add_course, name='add_course'),
    path('edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    # Staff URLs
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    # Subject URLs
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
]

