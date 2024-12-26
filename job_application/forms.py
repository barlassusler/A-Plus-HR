# forms.py

from django import forms
from .models import Candidate, Application, Location, Position

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'full_name', 'birth_date', 'phone_number',
            'residence_city', 'residence_district',
            'education_level', 'school_name', 'department_name'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    # Adayı burada gizli alıyoruz
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    # İstenilen pozisyonlar ve lokasyonlar
    desired_locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Çalışmak istediğiniz lokasyonlar"
    )

    applied_positions = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Başvurmak istediğiniz pozisyonlar"
    )

    class Meta:
        model = Application
        fields = ['resume', 'applied_positions', 'desired_locations']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Querysetlerin her zaman güncel olmasını sağla
        self.fields['desired_locations'].queryset = Location.objects.all()
        self.fields['applied_positions'].queryset = Position.objects.all()

    def save(self, commit=True):
        # Application objesini oluşturuyoruz
        instance = super().save(commit=False)

        # Eğer Candidate yoksa, onu oluşturuyoruz
        if not instance.candidate:
            candidate_form = CandidateForm(self.data)
            if candidate_form.is_valid():
                candidate = candidate_form.save()  # Yeni Candidate kaydediyoruz
                instance.candidate = candidate
            else:
                raise forms.ValidationError("Aday bilgileri geçersiz.")

        # Candidate ile ilişkilendirilmiş Application kaydını yapıyoruz
        if commit:
            instance.save()  # Application'ı kaydediyoruz
            self.save_m2m()  # Many-to-Many alanları kaydediyoruz

        return instance
