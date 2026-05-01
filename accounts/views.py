from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberCreationForm, MemberProfileForm
from .models import UserProfile

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin'):
            return redirect('admin_dashboard')
        elif hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'member':
            return redirect('member_dashboard')
        return redirect('member_login')
    return render(request, 'home.html')

def member_login(request):
    if request.user.is_authenticated:
        return redirect('member_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.userprofile.role == 'member':
            login(request, user)
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Invalid credentials or user is not a member')
    
    return render(request, 'member_login.html')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        # Allow superusers or users with admin role
        if user is not None and (user.is_superuser or user.userprofile.role == 'admin'):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or user is not an admin')
    
    return render(request, 'admin_login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.userprofile.role == 'admin'):
        return redirect('home')
    
    from projects.models import Project
    from tasks.models import Task
    
    members = User.objects.filter(userprofile__role='member')
    total_members = members.count()
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    
    context = {
        'members': members,
        'total_members': total_members,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'username': request.user.username,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required(login_url='member_login')
def member_dashboard(request):
    if request.user.userprofile.role != 'member':
        return redirect('home')
    
    projects = request.user.projects.all()
    tasks = request.user.assigned_tasks.all()
    total_projects = projects.count()
    in_progress_projects = projects.filter(status='in_progress').count()
    completed_projects = projects.filter(status='completed').count()
    
    context = {
        'projects': projects,
        'tasks': tasks,
        'total_projects': total_projects,
        'in_progress_projects': in_progress_projects,
        'completed_projects': completed_projects,
    }
    return render(request, 'member_dashboard.html', context)

@login_required(login_url='member_login')
def edit_profile(request):
    user_profile = request.user.userprofile
    
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('member_dashboard')
    else:
        form = MemberProfileForm(instance=user_profile)
    
    context = {'form': form}
    return render(request, 'edit_profile.html', context)

@login_required(login_url='admin_login')
def add_member(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.userprofile.role = 'member'
            user.userprofile.save()
            messages.success(request, 'Member added successfully')
            return redirect('list_members')
    else:
        form = MemberCreationForm()
    
    context = {'form': form}
    return render(request, 'add_member.html', context)

@login_required(login_url='admin_login')
def list_members(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    members = User.objects.filter(userprofile__role='member')
    context = {'members': members}
    return render(request, 'list_members.html', context)

@login_required(login_url='admin_login')
def delete_member(request, member_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
        return redirect('home')
    
    member = get_object_or_404(User, id=member_id, userprofile__role='member')
    member.delete()
    messages.success(request, 'Member deleted successfully')
    return redirect('list_members')