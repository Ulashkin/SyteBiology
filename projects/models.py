from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
class Project(models.Model):

    CATEGORY_CHOICES = [
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
        
    ]
     
    name = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='projects/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    file = models.FileField(upload_to='project_files/', blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True) 
    description2 = models.TextField()
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='Без імені')
    comment = models.TextField(default='Без коментаря')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class User(models.Model):
      username = models.CharField(max_length=150)
      email = models.EmailField()
      def __str__(self):
         return self.username
      
      

class UploadedFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
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
    
    
   