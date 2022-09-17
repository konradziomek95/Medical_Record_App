"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from med_record_app.views import (RegisterMedUserView,
                                  HomepageView,
                                  LoginView,
                                  ListOfLocations,
                                  CreateLocationView,
                                  ListOfPatients,
                                  CreatePatientView,
                                  DeletePatient)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage', HomepageView.as_view(), name='homepage'),
    path('register/', RegisterMedUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('location/add', CreateLocationView.as_view(), name='create_location'),
    path('location/list', ListOfLocations.as_view(), name='list_of_locations'),
    path('patient/add', CreatePatientView.as_view(), name='create_patient'),
    path('patient/list', ListOfPatients.as_view(), name='list_of_patients'),
    path('patient/delete/<int:id>', DeletePatient.as_view(), name ='delete_patient'),

]
