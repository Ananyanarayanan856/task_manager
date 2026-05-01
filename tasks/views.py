from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm, TaskStatusUpdateForm
from projects.models import Project

@login_required(login_url='admin_login')
def create_task(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully')
            return redirect('list_tasks')
    else:
        form = TaskForm()
    
    context = {'form': form}
    return render(request, 'create_task.html', context)

@login_required(login_url='admin_login')
def list_tasks(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'list_tasks.html', context)

@login_required(login_url='admin_login')
def edit_task(request, task_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully')
            return redirect('list_tasks')
    else:
        form = TaskForm(instance=task)
    
    context = {'form': form, 'task': task}
    return render(request, 'edit_task.html', context)

@login_required(login_url='admin_login')
def delete_task(request, task_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully')
    return redirect('list_tasks')

@login_required(login_url='member_login')
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Only assigned member or admin can update status
    if request.user != task.assigned_to and not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    if request.method == 'POST':
        form = TaskStatusUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task status updated successfully')
            return redirect('member_dashboard')
    else:
        form = TaskStatusUpdateForm(instance=task)
    
    context = {'form': form, 'task': task}
    return render(request, 'update_task_status.html', context)

@login_required(login_url='member_login')
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {'task': task}
    return render(request, 'view_task.html', context)