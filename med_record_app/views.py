from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView
from .forms import (RegisterMedUSerForm,
                    LoginForm,
                    MedicalRecordForm)
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .models import MedUser, Location, Patient, MedicalRecord


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


class ListOfLocations(ListView):
    model = Location
    template_name = 'med_record_app/location_list.html'


class CreateLocationView(CreateView):
    model = Location
    fields = ['name', 'address']
    template_name = 'med_record_app/add_location.html'
    success_url = reverse_lazy('list_of_locations')


class AddMedUserToLocation(View):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        ctx = {'locations': locations}
        return render(request, 'med_record_app/add_user_to_location.html', ctx)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        location_id = request.POST.get('location')
        location = get_object_or_404(Location, pk=int(location_id))
        location.workers_list.add(user)
        location.save()
        return redirect('list_of_locations')


class ListOfPatients(ListView):
    model = Patient
    template_name = 'med_record_app/patients_list.html'
    ordering = ['last_name']


class CreatePatientView(CreateView):
    model = Patient
    fields = ['first_name', 'last_name', 'PESEL']
    template_name = 'med_record_app/add_patient.html'
    success_url = reverse_lazy('list_of_patients')


class DeletePatient(View):
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


class UpdatePatient(UpdateView):
    model = Patient
    fields = '__all__'
    template_name_suffix = '_update_form'


class PatientDetailsView(DetailView):
    model = Patient


class CreateMedicalRecord(View):
    form_class = MedicalRecordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {'form': form}
        return render(request, 'med_record_app/add_medical_record.html', ctx)

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
