from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='projects/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    file = models.FileField(upload_to='project_files/', blank=True, null=True)
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