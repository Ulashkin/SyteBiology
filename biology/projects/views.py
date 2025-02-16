from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login 
from .forms import UserRegistrationForm, ProjectForm, OrderForm
from .models import Project, Order

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
    projects = Project.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'projects/admin_projects_list.html', {'projects': projects})
        else:
            return render(request, 'projects/user_projects_list.html', {'projects': projects})
    else:
        return render(request, 'projects/public_projects_list.html', {'projects': projects})
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
            return redirect('projects_list')
    else:
        form = OrderForm()
    return render(request, 'projects/make_order.html', {'form': form, 'project': project})
@login_required
def profile(request):
    user = request.user
    return render(request, 'projects/profile.html', {'user': user})