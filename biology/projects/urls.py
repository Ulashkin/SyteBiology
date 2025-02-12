from django.urls import path
from .views import register, projects_list, project_edit, project_delete


urlpatterns = [
    path('register/', register, name='register'),
    path('', projects_list, name='projects_list'),
    path('edit/<int:pk>/', project_edit, name='project_edit'),
    path('delete/<int:pk>/', project_delete, name='project_delete'),
]

