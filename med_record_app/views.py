from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView
from .forms import (RegisterMedUSerForm,
                    LoginForm,
                    MedicalRecordForm,
                    ReservationForm,
                    WorkDayForm)
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MedUser, Location, Patient, MedicalRecord, WorkDay, Reservation
from django.http import HttpResponse


# Create your views here.
class HomepageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'med_record_app/homepage.html')


class RegisterMedUserView(View):
    form_class = RegisterMedUSerForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {'form': form}
        return render(request, 'med_record_app/register.html', ctx)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = cd['login']
            password = cd['password1']
            first_name = cd['first_name']
            last_name = cd['last_name']
            profession = cd['profession']
            email = cd['email']
            PWZ = cd['PWZ']
            new_user = MedUser.objects.create_user(username=user,
                                                   password=password,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   profession=profession,
                                                   email=email,
                                                   PWZ=PWZ
                                                   )
            return redirect('/login/')
        ctx = {'form': form}
        return render(request, 'med_record_app/register.html', ctx)


class LoginView(FormView):
    template_name = 'med_record_app/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['login'], password=cd['password'])
        login(self.request, user)
        return response


class ListOfLocationsView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Location
    template_name = 'med_record_app/location_list.html'


class CreateLocationView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Location
    fields = ['name', 'address']
    template_name = 'med_record_app/add_location.html'
    success_url = reverse_lazy('list_of_locations')


class AddMedUserToLocationView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        locations = get_list_or_404(Location)
        user = self.request.user
        ctx = {'locations': locations}
        return render(request, 'med_record_app/add_user_to_location.html', ctx)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        location_id = request.POST.get('location')
        location = get_object_or_404(Location, pk=int(location_id))
        location.workers_list.add(user)
        location.save()
        return redirect('list_of_locations')


class ListOfPatientsView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Patient
    template_name = 'med_record_app/patients_list.html'
    ordering = ['last_name']


class CreatePatientView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Patient
    fields = ['first_name', 'last_name', 'PESEL']
    template_name = 'med_record_app/add_patient.html'
    success_url = reverse_lazy('list_of_patients')


class DeletePatientView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        patient = get_object_or_404(Patient, pk=id)
        warning = f'Do you reallly want to delate {patient.last_name} {patient.first_name} from database?'
        ctx = {'warning': warning,
               'patient': patient}
        return render(request, 'med_record_app/delete_patient.html', ctx)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        patient = get_object_or_404(Patient, pk=id)
        patient.delete()

        return redirect('list_of_patients')


class UpdatePatientView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Patient
    fields = '__all__'
    template_name_suffix = '_update_form'


class PatientDetailsView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Patient


class CreateMedicalRecordView(LoginRequiredMixin, View):
    login_url = '/login/'
    form_class = MedicalRecordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'med_record_app/add_medical_record.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        id = kwargs['id']
        if form.is_valid():
            cd = form.cleaned_data
            owner = self.request.user
            patient = get_object_or_404(Patient, pk=id)
            MedicalRecord.objects.create(patient=patient,
                                         owner=owner,
                                         diagnosis=cd['diagnosis'],
                                         ICD_10=cd['ICD_10'],
                                         symptoms=cd['symptoms'],
                                         tests=cd['tests'],
                                         imaging_examination=cd['imaging_examination'],
                                         description_of_IE=cd['description_of_IE'],
                                         medicines=cd['medicines'],
                                         medical_treatment=cd['medical_treatment'],
                                         home_recommendation=cd['home_recommendation']
                                         )
            return redirect('list_of_patients')
        return render(request, 'med_record_app/add_medical_record.html', {'form': form})


class CreateWorkDayView(LoginRequiredMixin, View):
    login_url = '/login/'
    form_class = WorkDayForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'med_record_app/add_workday.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            owner = self.request.user
            WorkDay.objects.create(owner=owner,
                                   day=cd['day'],
                                   start=cd['start'],
                                   end=cd['end'],
                                   interval=cd['interval']
                                   )
            return redirect('list_of_patients')
        return render(request, 'med_record_app/add_workday.html', {'form': form})


class CreateReservationView(LoginRequiredMixin, View):
    login_url = '/login/'
    form_class = ReservationForm

    def get(self, request, *args, **kwargs):
        owner = self.request.user
        form = self.form_class(user=owner)
        patients = get_list_or_404(Patient)
        return render(request, 'med_record_app/add_reservation.html', {'form': form, 'patients': patients})

    def post(self, request, *args, **kwargs):
        owner = self.request.user
        patients = get_list_or_404(Patient)
        form = self.form_class(self.request.POST, user=owner)
        patient = request.POST.get('patient')

        if form.is_valid():
            cd = form.cleaned_data
            time_of_reservation = cd['time_of_reservation']
            Reservation.objects.create(owner=owner, patient_id=patient,
                                       time_of_reservation=time_of_reservation)
            return redirect('list_of_patients')

        return render(request, 'med_record_app/add_reservation.html', {'form': form, 'patients': patients})


class ListOfReservationsView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        reservations = get_list_or_404(Reservation, owner=user)

        return render(request, 'med_record_app/reservation_list.html', {'reservations': reservations})
