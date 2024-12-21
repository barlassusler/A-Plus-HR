from django import forms
from .models import JobRequest
from biko_hr.models import Location, Organization, Job

class TaskRequestForm(forms.ModelForm):
    class Meta:
        model = JobRequest
        fields = [
            'location', 'organization', 'task_name', 'new_task_name', 'work_type',
            'work_type', 'replacement_for',
            'request_reason', 'description', 'start_date', 'personnel_count',
            'experience_years', 'education', 'special_requirements'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }