from django.urls import path
from . import views

urlpatterns = [

    path('index/', views.index, name='index'),  # Home page to display scanned attendance
    path('scan/', views.scan, name='scan'),  # URL to scan faces
    path('ProfileError' ,views.ProfileError , name='ProfileError'),
    path('AnyError/' ,views.AnyError , name='AnyError'),
    path('profiles/', views.profiles, name='profiles'),  # Admin URL to view all profiles
    path('details/', views.details, name='details'),  # Admin URL for details of last scanned face
    path('ajax/', views.ajax, name='ajax'),  # URL for AJAX requests (if applicable)
    path('select-unit/', views.select_unit, name='select_unit'),
     # Student Profile URLs
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('students/', views.student_profile_list, name='student_profile_list'),
    path('students/create/', views.student_profile_create, name='student_profile_create'),
    path('students/update/<int:pk>/', views.student_profile_update, name='student_profile_update'),

    # Lecturer Profile URLs
    path('lecturers/', views.lecturer_profile_list, name='lecturer_profile_list'),
    path('lecturers/create/', views.lecturer_profile_create, name='lecturer_profile_create'),
    path('lecturers/update/<int:pk>/', views.lecturer_profile_update, name='lecturer_profile_update'),

    # Unit URLs
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/update/<int:pk>/', views.unit_update, name='unit_update'),
    path('register-units/', views.register_units, name='register_units'),

    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/update/<int:pk>/', views.course_update, name='course_update'),

    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/update/<int:pk>/', views.attendance_update, name='attendance_update'),

   path('attendance_detailed/<int:unit_id>/', views.unit_attendance_detailed, name='unit_specific_attendance_detailed'),
    path('attendance/<int:unit_id>/', views.unit_attendance, name='unit_attendance'),
    path('attendance/graph/<int:unit_id>/', views.attendance_graph, name='attendance_graph'),
    path('register/', views.register, name='register'),
    path('', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'), # dashboard for logged in student 
    path('profile/update/', views.update_profile, name='update_profile'),# profile for the logged in user
    path('loged_in_attendance/', views.student_attendance, name='student_attendance'), # attendances for logged in user student 
]

