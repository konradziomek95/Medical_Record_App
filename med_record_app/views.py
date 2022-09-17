from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView
from .forms import (RegisterMedUSerForm,
                    LoginForm)
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .models import MedUser, Location, Patient


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
            MedUser.objects.create_user(username=user,
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
        pass


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
        patient = Patient.objects.get(pk=int(id))
        warning = f'Do you reallly want to delate {patient.last_name} {patient.first_name} from database?'
        ctx = {'warning': warning,
               'patient': patient}
        return render(request, 'med_record_app/delete_patient.html', ctx)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        patient = Patient.objects.get(pk=id)
        patient.delete()

        return redirect('list_of_patients')

class UpdatePatient(UpdateView):
    pass
