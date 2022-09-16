from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from .forms import (RegisterMedUSerForm,
                    LoginForm)
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .models import MedUser


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
            login = cd['login']
            password = cd['password1']
            first_name = cd['first_name']
            last_name = cd['last_name']
            profession = cd['profession']
            email = cd['email']
            PWZ = cd['PWZ']
            MedUser.objects.create_user(username=login,
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
