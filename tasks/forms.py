from django import forms
from .models import Task
from django.utils import timezone
from django.core.exceptions import ValidationError

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")
        return due_date

class TaskStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'member_notes']
        widgets = {
            'member_notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your notes here...'}),
        }
        labels = {
            'status': 'Update Status',
            'member_notes': 'Your Notes'
        }