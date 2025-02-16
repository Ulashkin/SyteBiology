from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', default='default_image.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class User(models.Model):
      username = models.CharField(max_length=150)
      email = models.EmailField()
      def __str__(self):
         return self.username