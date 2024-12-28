from django import forms
from .models import JobRequest
from biko_hr.models import Location, Organization, IncubationJob

class TaskRequestForm(forms.ModelForm):
    # new_position_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # replacement_for = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # request_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = JobRequest
        fields = [
            'location', 'organization', 'position_type', 'position_name', 'new_position_name',
            'replacement_for', 'work_type', 'request_reason', 'description', 'desired_start_date', 'desired_personnel_count',
            'desired_experience_years', 'required_education_level', 'special_requirements',
            'request_status_hr', 'request_status_organization_manager'
        ]
        widgets = {
            'desired_start_date': forms.DateInput(attrs={'type': 'date'}),
        }