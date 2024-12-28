from django import forms
from biko_hr.models import Candidate, Application, Location, Position
from django import forms
from biko_hr.models import Application, Position, Location

# class JobApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = [
#             'application_date', 'status', 'uploaded_resume'
#         ]
#         widgets = {
#             'birth_date': forms.DateInput(attrs={'type': 'date'}),
#             'status': forms.TextInput,
#             'uploaded_resume': forms.FileInput,
#         }
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'name', 'surname', 'birth_date', 'email', 'phone', 'experience', 'skills',
            'residence_city', 'residence_district',
            'education_level', 'school_name', 'department', 'desired_locations'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            # 'applied_positions': forms.CheckboxSelectMultiple,  # Çoklu seçim için widget
            'desired_locations': forms.CheckboxSelectMultiple,  # Çoklu seçim için widget
        }
    # İstenilen pozisyonlar ve lokasyonlar
    desired_locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Çalışmak istediğiniz lokasyonlar"
    )

    # applied_positions = forms.ModelMultipleChoiceField(
    #     queryset=Position.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     label="Başvurmak istediğiniz pozisyonlar"
    # )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Querysetlerin her zaman güncel olmasını sağla
        self.fields['desired_locations'].queryset = Location.objects.all()
        # self.fields['applied_positions'].queryset = Position.objects.all()

class ApplicationForm(forms.ModelForm):
    # # Adayı burada gizli alıyoruz
    # candidate = forms.ModelChoiceField(
    #     queryset=Candidate.objects.all(),
    #     widget=forms.HiddenInput(),
    #     required=False
    # )

    class Meta:
        model = Application
        fields = ['application_date','uploaded_resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['application_date'].widget = forms.DateInput(attrs={'type': 'date'})

    def save(self, commit=True):
        # Application objesini oluşturuyoruz
        instance = super().save(commit=False)

        # # Eğer Candidate yoksa, onu oluşturuyoruz
        # candidate = self.initial.get('candidate')
        # if candidate:
        #     instance.candidate = candidate
        # else:
        #     # If no candidate is provided, raise an error
        #     raise forms.ValidationError("No candidate associated with this application.")

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
