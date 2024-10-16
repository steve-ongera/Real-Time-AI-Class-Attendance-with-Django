from django.contrib import admin
from .models import *

# Registering models with the admin site
admin.site.register(StudentProfile)
admin.site.register(LecturerProfile)
admin.site.register(Semester)
admin.site.register(Unit)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(LastFace)
