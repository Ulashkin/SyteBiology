
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
        fields = ['name', 'description', 'file', 'image' ,'category','description2',]



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'comment']



class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file']


        from django import forms

class ProjectFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label='Фільтр за назвою')
    category = forms.ChoiceField(choices=[
        ('', 'Виберіть категорію'),
        ('5 клас', '5 клас'),
        ('6 клас', '6 клас'),
        ('7 клас', '7 клас'),
        ('8 клас', '8 клас'),
        ('9 клас', '9 клас'),
        ('10 клас', '10 клас'),
        ('11 клас', '11 клас'),
        ('Загальне', 'Загальне'),
        ('Виховання', 'Виховання'),
    ], required=False, label='Фільтр за категорією')

    from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()