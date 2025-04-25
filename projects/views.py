from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login 
from .forms import ProjectFilterForm, UserRegistrationForm, ProjectForm, OrderForm, FileUploadForm
from .models import Project, Order, UploadedFile, User
from .telegram_utils import send_telegram_message 
import logging
import mimetypes
from django.http import FileResponse
from django.core.exceptions import PermissionDenied
import asyncio
from django.contrib import messages
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_superuser

def home(request):
    context = {
        'teacher_name': "Ім'я вчителя",
        'work_experience': '12 років',
        'subjects': 'Біологія, Хімія',
        'description': 'Короткий опис про роботу вчителя',
    }
    return render(request, 'projects/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                
                return redirect('projects_list')

            except IntegrityError:  # Если имя или email уже есть
                messages.error(request, "Користувач з таким ім'ям або email вже існує.")
        
    else:
        form = UserRegistrationForm()

    return render(request, 'projects/register.html', {'form': form})
def projects_list(request):
    form = ProjectFilterForm(request.GET)
    projects = Project.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        category = form.cleaned_data.get('category')
        
        if name:
            projects = projects.filter(name__icontains=name)
        if category:
            projects = projects.filter(category=category)
    
    template = 'projects/public_projects_list.html'
    if request.user.is_authenticated:
        template = 'projects/admin_projects_list.html' if request.user.is_superuser else 'projects/user_projects_list.html'
    
    return render(request, template, {'projects': projects, 'form': form})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_edit.html', {'form': form})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('projects_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def make_order(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.project = project
            order.save()

            chat_id = '739291248'
            message = f"Новий запит на замовлення: {project.name}\nІм'я: {order.name}\nКоментар: {order.comment}\nЕлектронна пошта: {order.user.email}"
            
            asyncio.run(send_telegram_message(chat_id, message))
            messages.success(request, "Дякуємо за замовлення! Ми зв'яжемося з вами найближчим часом.")

            #return redirect('projects_list')

    else:
        form = OrderForm()
    return render(request, 'projects/make_order.html', {'form': form, 'project': project})

@login_required
def profile(request):
    return render(request, 'projects/profile.html', {'user': request.user})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'projects/upload_file.html', {'form': form})

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'projects/file_list.html', {'files': files})

def about(request):
    return render(request, 'projects/about.html')

def contact(request):
    return render(request, 'projects/contact.html')

def view_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    mime_type, _ = mimetypes.guess_type(file.file.path)
    mime_type = mime_type or "application/octet-stream"
    
    response = FileResponse(file.file.open('rb'), content_type=mime_type)
    response['Content-Disposition'] = 'inline'
    return response

def filter_projects(request):
    form = ProjectFilterForm(request.GET)
    projects = Project.objects.all()
    
    if form.is_valid():
        name = form.cleaned_data.get('name')
        category = form.cleaned_data.get('category')
        
        if name:
            projects = projects.filter(name__icontains=name)
        if category:
            projects = projects.filter(category=category)
    
    return render(request, 'projects/projects.html', {'form': form, 'projects': projects})
