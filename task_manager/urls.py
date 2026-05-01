from django.contrib import admin
from django.urls import path
from accounts import views as account_views
from projects import views as project_views
from tasks import views as task_views

urlpatterns = [
    # Home and Auth
    path('', account_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('member-login/', account_views.member_login, name='member_login'),
    path('admin-login/', account_views.admin_login, name='admin_login'),
    path('logout/', account_views.logout_view, name='logout'),
    
    # Dashboards
    path('member-dashboard/', account_views.member_dashboard, name='member_dashboard'),
    path('admin-dashboard/', account_views.admin_dashboard, name='admin_dashboard'),
    
    # Profile Management (Member)
    path('edit-profile/', account_views.edit_profile, name='edit_profile'),
    
    # Members Management (Admin)
    path('add-member/', account_views.add_member, name='add_member'),
    path('list-members/', account_views.list_members, name='list_members'),
    path('delete-member/<int:member_id>/', account_views.delete_member, name='delete_member'),
    
    # Projects Management (Admin)
    path('add-project/', project_views.add_project, name='add_project'),
    path('list-projects/', project_views.list_projects, name='list_projects'),
    path('project/<int:project_id>/', project_views.view_project, name='view_project'),
    path('project/<int:project_id>/edit/', project_views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', project_views.delete_project, name='delete_project'),
    
    # Tasks Management (Admin)
    path('create-task/', task_views.create_task, name='create_task'),
    path('list-tasks/', task_views.list_tasks, name='list_tasks'),
    path('edit-task/<int:task_id>/', task_views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', task_views.delete_task, name='delete_task'),
    
    # Tasks Management (Member)
    path('update-task-status/<int:task_id>/', task_views.update_task_status, name='update_task_status'),
    path('view-task/<int:task_id>/', task_views.view_task, name='view_task'),
]