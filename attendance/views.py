from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
import face_recognition
import cv2
import numpy as np
import winsound
from django.db.models import Q
from playsound import playsound
import os
from django.db.models import Prefetch
from django.db.models import Count
from django.db.models.functions import ExtractWeek
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CustomRegisterForm
from django.contrib import messages


# Path for sound notification
current_path = os.path.dirname(__file__)
sound_folder = os.path.join(current_path, 'sound/')
sound = os.path.join(sound_folder, 'beep-30b.wav')

# Global variable for last recognized face
last_face = 'no_face'

def index(request):
    """Render the homepage with the latest scanned faces and attendance status."""
    scanned = LastFace.objects.all().order_by('date').reverse()
    present_students = Attendance.objects.filter(present=True).order_by('date').reverse()
    absent_students = Attendance.objects.filter(present=False).order_by('date')
    
    context = {
        'scanned': scanned,
        'present_students': present_students,
        'absent_students': absent_students,
    }
    return render(request, 'core/index.html', context)


def scan(request):
    global last_face

    # Check if unit_id and week are provided in the request
    unit_id = request.GET.get('unit_id')  # Expecting unit_id as a query parameter
    week = request.GET.get('week')  # Expecting week as a query parameter

    # Validate parameters
    if not unit_id or not week:
        return HttpResponse("Unit or week not specified.")  # Return error if parameters are missing

    # Fetch the unit from the database
    try:
        unit = Unit.objects.get(id=unit_id)  # Get the Unit instance
    except Unit.DoesNotExist:
        return HttpResponse("Unit not found.")  # Handle unit not found

    known_face_encodings = []
    known_face_names = []

    # Load known faces and their encodings
    profiles = StudentProfile.objects.all()
    for profile in profiles:
        person = profile.image
        image_of_person = face_recognition.load_image_file(f'media/{person}')
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{profile.first_name} {profile.last_name}')  # Use full name

    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        if not ret:  # Ensure the frame was captured successfully
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    # Find the corresponding StudentProfile
                    try:
                        student_profile = StudentProfile.objects.get(
                            first_name=name.split()[0],
                            last_name=name.split()[1]
                        )
                        student = Student.objects.get(profile=student_profile)

                        # Update attendance record
                        attendance_record, created = Attendance.objects.get_or_create(
                            student=student,
                            unit=unit,  # Use the unit instance obtained earlier
                            week=week,  # Use the week passed via the request
                            defaults={'present': True}
                        )
                        if not created:  # If record already exists, update it
                            attendance_record.present = True
                            attendance_record.save()

                        if last_face != name:
                            last_face = LastFace(profile=student_profile)
                            last_face.save()
                            last_face = name
                            winsound.PlaySound(sound, winsound.SND_ASYNC)


                         # Redirect to the student's profile page
                        return HttpResponseRedirect(reverse('student_profile', args=[student_profile.id]))    

                    except (StudentProfile.DoesNotExist, Student.DoesNotExist):
                        print(f"Profile not found for {name}")

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Taking Attendance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse('Scanner closed')




def student_profile(request, student_id):
    # Fetch the student profile using the student_id
    student_profile = get_object_or_404(StudentProfile, id=student_id)
    context = {
        'student_profile': student_profile
    }
    return render(request, 'students_profile.html', context)

def ajax(request):
    last_face = LastFace.objects.last()
    context = {
        'last_face': last_face
    }
    return render(request, 'core/ajax.html', context)



def profiles(request):
    """View to display all student profiles."""
    profiles = StudentProfile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'core/profiles.html', context)


def details(request):
    """View the details of the last scanned face."""
    try:
        last_face_entry = LastFace.objects.last()
        profile = last_face_entry.profile if last_face_entry else None
    except:
        profile = None

    context = {
        'profile': profile
    }
    return render(request, 'core/details.html', context)

# View for creating and listing student profiles
def student_profile_list(request):
    students = StudentProfile.objects.all()
    return render(request, 'profiles/student_profile_list.html', {'students': students})


def student_profile_create(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_profile_list')
    else:
        form = StudentProfileForm()
    return render(request, 'profiles/student_profile_form.html', {'form': form})


def student_profile_update(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_profile_list')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'profiles/student_profile_form.html', {'form': form, 'student': student})


# View for creating and listing lecturer profiles
def lecturer_profile_list(request):
    lecturers = LecturerProfile.objects.all()
    return render(request, 'profiles/lecturer_profile_list.html', {'lecturers': lecturers})


def lecturer_profile_create(request):
    if request.method == 'POST':
        form = LecturerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lecturer_profile_list')
    else:
        form = LecturerProfileForm()
    return render(request, 'profiles/lecturer_profile_form.html', {'form': form})


def lecturer_profile_update(request, pk):
    lecturer = get_object_or_404(LecturerProfile, pk=pk)
    if request.method == 'POST':
        form = LecturerProfileForm(request.POST, request.FILES, instance=lecturer)
        if form.is_valid():
            form.save()
            return redirect('lecturer_profile_list')
    else:
        form = LecturerProfileForm(instance=lecturer)
    return render(request, 'profiles/lecturer_profile_form.html', {'form': form})


# View for creating and listing units
def unit_list(request):
    units = Unit.objects.all()
    weeks = list(range(1, 11))  # Create a list of weeks from 1 to 1
    return render(request, 'units/unit_list.html', {'units': units, 'weeks': weeks})


def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm()
    return render(request, 'units/unit_form.html', {'form': form})


def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'units/unit_form.html', {'form': form})


# View for creating and listing courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})


def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})


# View for creating and listing attendance records
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})


def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_form.html', {'form': form})


def attendance_update(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance/attendance_form.html', {'form': form})

# views.py

from django.shortcuts import render, redirect
from .forms import SelectUnitForm

def select_unit(request):
    if request.method == "POST":
        form = SelectUnitForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data['unit_code']
            # Redirect to scan with the unit passed as a query parameter
            return redirect('scan')  # Update with the actual URL name for your scan view
    else:
        form = SelectUnitForm()

    return render(request, 'select_unit.html', {'form': form})




def extract_week_number(week_string):
    """
    Extract the week number from various possible formats.
    Returns -1 if no valid number is found.
    """
    try:
        # Try to extract a number from the string
        return int(''.join(filter(str.isdigit, week_string)))
    except ValueError:
        # If no valid number is found, return -1
        return -1

#this view shows detailed table for class attendance

def unit_attendance_detailed(request, unit_id=None):
    # Get all units or a specific unit if unit_id is provided
    if unit_id:
        units = Unit.objects.filter(id=unit_id)
    else:
        units = Unit.objects.all()

    # Get all students
    students = Student.objects.all().prefetch_related(
        Prefetch('attendance_set', queryset=Attendance.objects.order_by('week'))
    )

    # Get all unique weeks and sort them numerically
    weeks = Attendance.objects.values_list('week', flat=True).distinct()
    weeks = sorted(weeks, key=extract_week_number)

    # Prepare data for the template
    units_data = []
    for unit in units:
        unit_data = {
            'id': unit.id,  # Include the unit ID
            'unit_name': unit.unit_name,
            'unit_code': unit.unit_code,
            'students': []
        }
        for student in students:
            student_data = {
                'name': f"{student.profile.first_name} {student.profile.last_name}",
                'attendance': {}
            }
            for week in weeks:
                attendance = Attendance.objects.filter(
                    student=student,
                    unit=unit,
                    week=week
                ).first()
                student_data['attendance'][week] = 'Present' if attendance and attendance.present else 'Absent'
            unit_data['students'].append(student_data)
        units_data.append(unit_data)

    context = {
        'units_data': units_data,
        'weeks': weeks,
    }
    return render(request, 'unit_attendance_table.html', context)

def extract_week_number(week_string):
    return int(''.join(filter(str.isdigit, week_string)))

def attendance_graph(request, unit_id):
    unit = Unit.objects.get(id=unit_id)
    
    # Get attendance data grouped by week
    attendance_data = Attendance.objects.filter(unit=unit).values('week').annotate(
        present_count=Count('id', filter=models.Q(present=True)),
        absent_count=Count('id', filter=models.Q(present=False))
    )
    
    # Sort the data by week number
    sorted_data = sorted(attendance_data, key=lambda x: extract_week_number(x['week']))
    
    # Prepare data for the graph
    weeks = []
    present_counts = []
    absent_counts = []
    
    for entry in sorted_data:
        weeks.append(extract_week_number(entry['week']))  # Store only the number
        present_counts.append(entry['present_count'])
        absent_counts.append(entry['absent_count'])
    
    context = {
        'unit': unit,
        'weeks': weeks,
        'present_counts': present_counts,
        'absent_counts': absent_counts,
    }
    
    return render(request, 'attendance_graph.html', context)



# Register View
def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            # Process the form data and save the user
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to login or wherever you need
        else:
            # If form is not valid, add specific error messages
            messages.error(request, "There was an error with your submission. Please correct the errors and try again.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = CustomRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

# Login View
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Add a success message
            messages.success(request, 'Login successful! Welcome to your dashboard.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
            return redirect('login')
    return render(request, 'registration/login.html')

# Logout View
def custom_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully !')
    return redirect('login')

@login_required
def dashboard(request):
    try:
        # Fetch the student's profile using the logged-in user's username
        student_profile = StudentProfile.objects.get(user_name=request.user.username)

        # Pass the student's profile to the dashboard template
        context = {
            'student_profile': student_profile
        }
        return render(request, 'dashboard.html', context)
    
    except StudentProfile.DoesNotExist:
        # If no profile is found, redirect to the error page
        messages.error(request, 'Logged in successful but Your profile not found contact Admin.')
        return render(request, 'error.html')
    


@login_required
def update_profile(request):
    # Fetch the student's profile based on the logged-in user
    student_profile = get_object_or_404(StudentProfile, user_name=request.user.username)

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after successful update
    else:
        form = StudentProfileUpdateForm(instance=student_profile)

    context = {
        'form': form,
        'student_profile': student_profile
    }
    return render(request, 'update_profile.html', context)

def student_attendance(request):
    if request.user.is_authenticated:
        try:
            # Get the logged-in user's student profile based on user_name
            student_profile = StudentProfile.objects.get(user_name=request.user.username)
            
            # Get the student instance associated with this profile
            student = Student.objects.get(profile=student_profile)

            # Retrieve the attendance records for the student
            attendance_records = Attendance.objects.filter(student=student).select_related('unit')

            # Retrieve unique units the student has attendance records for
            unique_units = {record.unit for record in attendance_records}

            # Calculate attendance percentage and exam eligibility
            unit_attendance_info = {}
            for unit in unique_units:
                unit_records = attendance_records.filter(unit=unit)
                total_classes = unit_records.count()
                attended_classes = unit_records.filter(present=True).count()

                if total_classes > 0:
                    attendance_percentage = (attended_classes / total_classes) * 100
                    eligible_for_exams = attendance_percentage >= 60
                    bonus_marks = 10 if eligible_for_exams else 0

                    unit_attendance_info[unit] = {
                        'attendance_percentage': round(attendance_percentage, 2),  # Round to 2 decimal places
                        'eligible_for_exams': eligible_for_exams,
                        'bonus_marks': bonus_marks,
                    }

            context = {
                'unique_units': unique_units,
                'unit_attendance_info': unit_attendance_info,  # Include attendance information
            }
            return render(request, 'student_attendance.html', context)
        except StudentProfile.DoesNotExist:
            return render(request, 'student_attendance.html', {'error': 'Student profile not found.'})
        except Student.DoesNotExist:
            return render(request, 'student_attendance.html', {'error': 'Student not found.'})
    else:
        return render(request, 'student_attendance.html', {'error': 'User not authenticated.'})

    
#get units for specific user

def unit_attendance(request, unit_id):
    if request.user.is_authenticated:
        try:
            # Get the logged-in user's student profile
            student_profile = StudentProfile.objects.get(user_name=request.user.username)
            student = Student.objects.get(profile=student_profile)

            # Retrieve attendance records for the specific unit
            attendance_records = Attendance.objects.filter(student=student, unit_id=unit_id)

            # Calculate total classes and attended classes
            total_classes = attendance_records.count()  # Total number of attendance records
            attended_classes = attendance_records.filter(present=True).count()  # Count of attended classes

            # Calculate attendance percentage
            attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0

            # Determine eligibility for exams and bonus marks
            eligible_for_exams = attendance_percentage >= 60
            bonus_marks = 10 if eligible_for_exams else 0

            context = {
                'attendance_records': attendance_records,
                'unit_id': unit_id,  # You can use this in the template for unit details
                'attendance_percentage': attendance_percentage,
                'eligible_for_exams': eligible_for_exams,
                'bonus_marks': bonus_marks,
            }
            return render(request, 'unit_attendance.html', context)
        except StudentProfile.DoesNotExist:
            return render(request, 'unit_attendance.html', {'error': 'Student profile not found.'})
        except Student.DoesNotExist:
            return render(request, 'unit_attendance.html', {'error': 'Student not found.'})
    else:
        return render(request, 'unit_attendance.html', {'error': 'User not authenticated.'})
