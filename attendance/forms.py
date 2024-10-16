from django import forms
from .models import *
# In yourapp/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



class SelectUnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_code']

# Form for StudentProfile
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'user_name', 'first_name', 'last_name', 'reg_no', 'phone', 'email', 
            'dob', 'course', 'religion', 'games', 'hostel', 'room_no', 
            'parents_phone', 'parents_name', 'address', 'image', 'role'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


# Form for LecturerProfile
class LecturerProfileForm(forms.ModelForm):
    class Meta:
        model = LecturerProfile
        fields = [
            'user_name', 'first_name', 'last_name', 'phone', 'email', 
            'dob', 'course', 'address', 'image', 'role'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


# Form for Unit
class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_code', 'unit_name', 'course', 'semester', 'year_of_study', 'lecturer']
        widgets = {
            'lecturer': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }


# Form for Course
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'units', 'semester']
        widgets = {
            'units': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }


# Form for Attendance
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'unit', 'week', 'present']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'week': forms.TextInput(attrs={'class': 'form-control'}),
            'present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['address', 'parents_phone', 'parents_name', 'religion']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'parents_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'parents_name': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
        }