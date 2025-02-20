
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project
from .models import Order
from .models import UploadedFile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'file']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'comment']



class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file']

class ProjectFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label='Фільтр за назвою')
    description = forms.ChoiceField(choices=[
        ('', 'Виберіть опис'),
        ('Ботаніка', 'Ботаніка'),
        ('Зоологія', 'Зоологія'),
        ('Анатомія', 'Анатомія')
    ], required=False, label='Фільтр за описом')
        