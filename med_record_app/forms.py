from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import MedUser, PROFESSION, Location, MedicalRecord, Patient, Reservation, WorkDay, DAY
import datetime


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


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


class ReservationForm(forms.Form):
    time_of_reservation = forms.DateTimeField(widget=DateTimePickerInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_time_of_reservation(self):
        user = self.user
        cd = super().clean()
        time_of_reservation = cd.get('time_of_reservation')
        day_of_reservation = datetime.datetime.isoweekday(time_of_reservation)
        if not WorkDay.objects.filter(owner=user).filter(day=day_of_reservation).exists():
            raise ValidationError('Office is closed that day')
        work_day = WorkDay.objects.get(day=day_of_reservation)
        start = work_day.start
        end = work_day.end
        interval = work_day.interval
        last_visit_delta = datetime.timedelta(hours=end.hour,
                                              minutes=end.minute) - datetime.timedelta(minutes=interval)
        last_visit_date = (datetime.datetime.min + last_visit_delta).time()
        if time_of_reservation.time() < start or time_of_reservation.time() > last_visit_date:
            raise ValidationError('booking time outside working hours')
        start_date = time_of_reservation - datetime.timedelta(minutes=interval - 1)
        end_date = time_of_reservation + datetime.timedelta(minutes=interval - 1)
        if Reservation.objects.filter(time_of_reservation__range=(start_date, end_date)).exists():
            raise ValidationError('booking time conflicts with another visit')
        return time_of_reservation


class WorkDayForm(forms.Form):
    day = forms.ChoiceField(choices=DAY)
    start = forms.TimeField(widget=TimePickerInput())
    end = forms.TimeField(widget=TimePickerInput())
    interval = forms.IntegerField(min_value=0)

