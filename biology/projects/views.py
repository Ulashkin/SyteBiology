from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login 
from .forms import ProjectFilterForm, UserRegistrationForm, ProjectForm, OrderForm
from .models import Project, Order
from .telegram_utils import send_telegram_message 
import logging
import asyncio
from .forms import FileUploadForm
from .models import UploadedFile

logger = logging.getLogger(__name__)
def is_admin(user):
    return user.is_superuser

def home(request):
    context = {
        'teacher_name': 'Ім\'я вчителя',
        'work_experience': '12 років',
        'subjects': 'Біологія, Хімія',
        'description': 'Короткий опис про роботу вчителя',
    }
    return render(request, 'projects/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projects_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'projects/register.html', {'form': form})

def projects_list(request):
    form = ProjectFilterForm(request.GET)
    projects = Project.objects.all()

    if form.is_valid():
        print("Форма дійсна")
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')
        
        if name:
            projects = projects.filter(name__icontains=name)
        if description:
            projects = projects.filter(description__icontains=description)
        print("Знайдено проекти:", projects)
    else:
        print("Форма недійсна:", form.errors)

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'projects/admin_projects_list.html', {'projects': projects, 'form': form})
        else:
            return render(request, 'projects/user_projects_list.html', {'projects': projects, 'form': form})
    else:
        return render(request, 'projects/public_projects_list.html', {'projects': projects, 'form': form})
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

          
            logger.info(f"Order saved: {order.id}")
            print(f"Order saved: {order.id}")

            
            chat_id = '739291248'  
            message = f"Новий запит на замовлення: {project.name}\nІм'я: {order.name}\nКоментар: {order.comment}\nЕлектронна пошта: {order.user.email}"

            try:
                asyncio.run(send_telegram_message(chat_id, message))
                logger.info(f"Повідомлення відправлено: {message}")
                print(f"Повідомлення відправлено: {message}")
            except Exception as e:
                logger.error(f"Помилка відправки повідомлення: {e}")
                print(f"Помилка відправки повідомлення: {e}")

            return redirect('projects_list')
    else:
        form = OrderForm()
    return render(request, 'projects/make_order.html', {'form': form, 'project': project})
@login_required
def profile(request):
    user = request.user
    return render(request, 'projects/profile.html', {'user': user})

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
    return render(request, 'upload_file.html', {'form': form})

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})


def about(request):
    return render(request, 'projects/about.html')

def contact(request):
    return render(request, 'projects/contact.html')