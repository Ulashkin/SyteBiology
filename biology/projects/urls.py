from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, upload_file,contact,about,  file_list, project_detail, projects_list, project_edit, project_delete, project_create, home, profile, make_order
from django.contrib.auth.models import User
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', projects_list, name='projects_list'),
    path('edit/<int:pk>/', project_edit, name='project_edit'),
    path('delete/<int:pk>/', project_delete, name='project_delete'),
    path('create/', project_create, name='project_create'),
   # path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('make_order/<int:pk>/', make_order, name='make_order'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
     path('projects/', projects_list, name='projects_list'),
      path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
     path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    
]
