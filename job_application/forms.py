from django import forms
from .models import JobApplication, Position, Location

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'resume', 'full_name', 'birth_date', 'phone_number',
            'residence_city', 'residence_district',
            'education_level', 'school_name', 'department_name',
            'applied_positions', 'desired_locations'  # Bu alanlar eklendi
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'applied_positions': forms.CheckboxSelectMultiple,  # Çoklu seçim için widget
            'desired_locations': forms.CheckboxSelectMultiple,  # Çoklu seçim için widget
        }

