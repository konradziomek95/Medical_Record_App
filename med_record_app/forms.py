from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import MedUser, PROFESSION, Location, MedicalRecord, Patient


class RegisterMedUSerForm(forms.Form):
    login = forms.CharField(max_length=128)
    password1 = forms.CharField(label='password', max_length=64)
    password2 = forms.CharField(label='re-enter password', max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    profession = forms.ChoiceField(choices=PROFESSION)
    email = forms.EmailField()
    PWZ = forms.CharField(max_length=10)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Passwords do not match!')

    def clean_login(self):
        login = self.cleaned_data['login']
        if MedUser.objects.filter(username=login).exists():
            raise ValidationError('User with this login already exists.')
        return login


class LoginForm(forms.Form):
    login = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = super().clean()
        login = cd.get('login')
        password = cd.get('password')
        user = authenticate(username=login, password=password)
        if user is None:
            raise ValidationError('Wrong login or password!')
        self.user = user


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        exclude = ['patient', 'owner', 'date']
