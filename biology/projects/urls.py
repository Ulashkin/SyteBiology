from django.urls import path
from .views import home, register, projects_list, project_edit, project_delete, project_create
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('', projects_list, name='projects_list'),
    path('edit/<int:pk>/', project_edit, name='project_edit'),
    path('delete/<int:pk>/', project_delete, name='project_delete'),
    path('create/', project_create, name='project_create'),
    path('home/', home, name='home'),
  
    #path('projects/', views.project_list, name='project_list'),
    
]


