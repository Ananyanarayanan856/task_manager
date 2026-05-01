from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'status', 'created_at']
    list_filter = ['status', 'project', 'created_at']
    search_fields = ['title', 'assigned_to__username']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)