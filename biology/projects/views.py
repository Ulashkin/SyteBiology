
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, ProjectForm
from .models import Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


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


@login_required
def projects_list(request):
    projects = Project.objects.filter(author=request.user)
    return render(request, 'projects/projects_list.html', {'projects': projects})
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

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'project': projects})

def home(request):
    context = {
        'teacher_name': 'Імя вчителя',
        'work_experience': '12 років',
        'subjects': 'Біологія, Хімія',
        'description': 'Короткий опис про роботу вчителя',
    }
    return render(request, 'projects/home.html', context)
