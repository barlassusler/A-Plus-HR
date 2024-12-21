from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password",
    )
    user_type = forms.ChoiceField(choices=[('hr_staff', 'HR Staff'), ('organization_staff', 'Organization Staff')])


    class Meta:
        model = User
        fields = ["username",'email', "first_name", "last_name", 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data