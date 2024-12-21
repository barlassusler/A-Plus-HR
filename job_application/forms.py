from django import forms
from biko_hr.models import Application, Position, Location

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'application_date', 'status', 'uploaded_resume'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.TextInput,
            'uploaded_resume': forms.FileInput,
        }

