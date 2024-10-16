from django.db import models
from django.contrib.auth.models import AbstractUser


# Roles for both Students and Lecturers
ROLES = [('student', 'Student'), ('lecturer', 'Lecturer'), ('admin', 'Admin')]

# Student Profile model
class StudentProfile(models.Model):
    user_name = models.CharField(max_length=300)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    reg_no = models.CharField(max_length=70)  # Registration number should be a CharField for alphanumeric codes
    phone = models.CharField(max_length=15)  # Using CharField to accommodate special characters like '+'
    email = models.EmailField()
    dob = models.DateField()  # Date of birth
    course = models.CharField(max_length=200)
    religion = models.CharField(max_length=70)
    games = models.CharField(max_length=70)
    hostel = models.CharField(max_length=70)
    room_no = models.CharField(max_length=70)
    parents_phone = models.CharField(max_length=15)  # CharField for phone
    parents_name = models.CharField(max_length=70)
    address = models.CharField(max_length=100)  # Increased length for more flexibility
    role = models.CharField(choices=ROLES, max_length=20, null=True, blank=False, default='student')
    image = models.ImageField(upload_to='profile_images/',null=True, blank=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.role}'


# Lecturer Profile model
class LecturerProfile(models.Model):
    user_name = models.CharField(max_length=300)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    phone = models.CharField(max_length=15)  # CharField for phone
    email = models.EmailField()
    dob = models.DateField()  # Date of birth
    course = models.CharField(max_length=200)
    address = models.CharField(max_length=100)  # Increased length for flexibility
    role = models.CharField(choices=ROLES, max_length=20, null=True, blank=False, default='lecturer')
    image = models.ImageField(upload_to='lec_images/')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.role}'




# Model for Semesters
class Semester(models.Model):
    name = models.CharField(max_length=50)  # e.g., 'Semester 1', 'Semester 2'
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Unit(models.Model):
    unit_code = models.CharField(max_length=10, unique=True)
    unit_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)  # Assuming this is just the name of the course here
    semester = models.CharField(max_length=20)  # e.g., 'Semester 1', 'Semester 2'
    year_of_study = models.IntegerField()  # e.g., 1st year, 2nd year, etc.
    lecturer = models.ForeignKey(LecturerProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'lecturer'})

    def __str__(self):
        return f'{self.unit_code} - {self.unit_name}'


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=200)
    units = models.ManyToManyField(Unit, related_name='courses')  # Added related_name here
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name



# Student Model (linked to the student profile)
class Student(models.Model):
    profile = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_of_study = models.IntegerField()

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name} - Year {self.year_of_study}'


# Model for Attendance Records
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    week = models.CharField(max_length=50)  # Added week field to track attendance by week
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.profile.first_name} {self.student.profile.last_name} - {self.unit.unit_code} on {self.date}'


# Last Face Recognition Attempt (for logging face recognition attempts)
class LastFace(models.Model):
    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name} - {self.date}'
