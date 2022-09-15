from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import RegisterMedUSerForm
from .models import MedUser


# Create your views here.


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
            MedUser.objects.create(username=login,
                                   password=password,
                                   first_name=first_name,
                                   last_name=last_name,
                                   profession=profession,
                                   email=email,
                                   PWZ=PWZ
                                   )
            return HttpResponse(f'{login} dodany')
        ctx = {'form': form}
        return render(request, 'med_record_app/register.html', ctx)
