from django import forms
from .models import Project
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(userprofile__role='member'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'due_date', 'members']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Project.objects.filter(name__iexact=name).exists():
            if self.instance and self.instance.pk:
                if not Project.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                    return name
            raise ValidationError("A project with this name already exists.")
        return name

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")
        return due_date