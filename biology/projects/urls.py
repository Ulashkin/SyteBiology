from django.urls import path
from .views import register, projects_list

urlpatterns = [
    path('register/', register, name='register'),
    path('', projects_list, name='projects_list'),
]