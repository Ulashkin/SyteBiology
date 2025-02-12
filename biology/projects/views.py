
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import UserRegistrationForm, ProjectForm
from .models import Project
from django.contrib.auth.decorators import login_required



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
