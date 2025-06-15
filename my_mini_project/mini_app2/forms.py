#mini_app2/form.py
from django import forms
class StudentLoginForm(forms.Form):
    student_id = forms.IntegerField(label='Student ID')
    password = forms.IntegerField(label='Password(DDMMYYYY)')


class TeacherRegistrationForm(forms.Form):
    teacher_id = forms.CharField(label='Teacher ID')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    section = forms.CharField(label='Section')



class TeacherLoginForm(forms.Form):
    teacher_id = forms.CharField(label='Teacher ID')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    section = forms.CharField(label='Section')

