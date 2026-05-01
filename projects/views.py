from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm

@login_required(login_url='admin_login')
def add_project(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()
            messages.success(request, 'Project added successfully')
            return redirect('list_projects')
    else:
        form = ProjectForm()
    
    context = {'form': form}
    return render(request, 'add_project.html', context)

@login_required(login_url='admin_login')
def list_projects(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'list_projects.html', context)

@login_required(login_url='admin_login')
def edit_project(request, project_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully')
            return redirect('list_projects')
    else:
        form = ProjectForm(instance=project)
    
    context = {'form': form, 'project': project}
    return render(request, 'edit_project.html', context)

@login_required(login_url='admin_login')
def delete_project(request, project_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, 'Project deleted successfully')
    return redirect('list_projects')

@login_required(login_url='admin_login')
def view_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    context = {'project': project, 'tasks': tasks}
    return render(request, 'project_detail.html', context)