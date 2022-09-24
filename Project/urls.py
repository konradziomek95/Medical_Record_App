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
    1. Import  include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from med_record_app.views import (RegisterMedUserView,
                                  HomepageView,
                                  LoginView,
                                  LogoutView,
                                  LoggedInHomepageView,
                                  ListOfLocationsView,
                                  CreateLocationView,
                                  ListOfPatientsView,
                                  CreatePatientView,
                                  DeletePatientView,
                                  AddMedUserToLocationView,
                                  UpdatePatientView,
                                  CreateMedicalRecordView,
                                  PatientDetailsView,
                                  CreateReservationView,
                                  CreateWorkDayView,
                                  ListOfReservationsView,
                                  ListOfWorkDaysView,
                                  MedicalRecordView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', HomepageView.as_view(), name='homepage'),
    path('register/', RegisterMedUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/homepage/', LoggedInHomepageView.as_view(), name='user_homepage'),
    path('location/add/', CreateLocationView.as_view(), name='create_location'),
    path('location/list/', ListOfLocationsView.as_view(), name='list_of_locations'),
    path('patient/add/', CreatePatientView.as_view(), name='create_patient'),
    path('patient/list/', ListOfPatientsView.as_view(), name='list_of_patients'),
    path('patient/delete/<int:id>/', DeletePatientView.as_view(), name='delete_patient'),
    path('patient/update/<int:pk>/', UpdatePatientView.as_view(), name='update_patient'),
    path('patient/<int:id>/record/add/', CreateMedicalRecordView.as_view(), name='create_medical_record'),
    path('patient/details/<int:pk>/', PatientDetailsView.as_view(), name='patient_details'),
    path('location/user/', AddMedUserToLocationView.as_view(), name='add_user_to_location'),
    path('calendar/add/', CreateWorkDayView.as_view(), name='add_workday'),
    path('calendar/list/', ListOfWorkDaysView.as_view(), name='calendar'),
    path('reservation/add/', CreateReservationView.as_view(), name='create_reservation'),
    path('reservation/list/', ListOfReservationsView.as_view(), name='list_of_reservations'),
    path('record/details/<int:pk>/', MedicalRecordView.as_view(), name='record_details'),

]
