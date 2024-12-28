from django import forms
from jobrequest.models import JobRequest
from biko_hr.models import Location, Organization, IncubationJob

class JobRequestEvaluationForm(forms.ModelForm):
    class Meta:
        model = JobRequest
        fields = [
            'desired_personnel_count', # If wants to change or wants to decide the number of desired customers.
            'request_status_hr'
        ]
        widgets = {
            'desired_personnel_count': forms.IntegerField(attrs={'type': 'date'}),
        }
