import datetime

from django.test import TestCase
import pytest
from med_record_app.models import MedUser, Location, Patient
from datetime import date


# Create your tests here.
@pytest.mark.django_db
def test_homepage_view(client):
    response = client.get('/homepage/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user(client, django_user_model):
    user = django_user_model.objects.create_user(
        username='someone', password='password'
    )
    assert MedUser.objects.get(username='someone')


@pytest.mark.django_db
def test_login_view(client, user):
    data = {
        'login': user.username,
        'password': user.password
    }
    response = client.post('/login/', data)
    assert response.content


@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(username=user.username, password=user.password)
    response = client.get('/logout/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_logged_homepage_view(client, user):
    client.force_login(user)
    response = client.get('/user/homepage/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_location_view(client, user):
    data = {
        'name': 'location',
        'address': 'some address',
        'workers_list': user
    }
    client.force_login(user)
    response = client.post('/location/add/', data)
    assert response.status_code == 302
    assert Location.objects.get(name='location')


@pytest.mark.django_db
def test_list_of_locations_view(client, locations, user):
    client.force_login(user)
    response = client.get('/location/list/')
    locations = Location.objects.all()
    assert locations.count() == 3
    assert response.status_code == 200
    i = 0
    for location in response.context['object_list']:
        obj = locations[i]
        assert location == obj
        i += 1


@pytest.mark.django_db
def test_create_patient_view(client, user):
    date_birth = datetime.date.today()
    data = {
        'first_name': 'Adam',
        'last_name': 'Sam',
        'PESEL': '12345678911',
        'date_of_birth': date_birth,
        'address': 'address',
        'contact': 'contact'
    }
    client.force_login(user)
    response = client.post('/patient/add/', data)
    assert response.status_code == 302
    assert Patient.objects.get(last_name='Sam')


@pytest.mark.django_db
def test_ad_meduser_to_location_view(client, location, user):
    data = {
        'location': location.pk
    }
    client.force_login(user)
    response = client.post('/location/user/', data)
    assert response.status_code == 302
    assert Location.objects.get(name=location.name, workers_list=user)


@pytest.mark.django_db
def test_list_of_patients_view(client, user, patients):
    client.force_login(user)
    response = client.get('/patient/list/')
    patients = Patient.objects.all().order_by('last_name')
    assert patients.count() == 3
    assert response.status_code == 200
    i = 0
    for patient in response.context['object_list']:
        assert patient == patients[i]
        i += 1


@pytest.mark.django_db
def test_delete_patient_view(client, user):
    patient = Patient.objects.create(first_name='Zofia', last_name='Nieznana', PESEL='95030107755')
    assert Patient.objects.get(first_name='Zofia', last_name='Nieznana', PESEL='95030107755')
    data = {
        'patient': patient
    }
    client.force_login(user)
    response = client.post(f'/patient/delete/{patient.pk}/', data)
    assert response.status_code == 302
    assert Patient.objects.filter(first_name='Zofia', last_name='Nieznana', PESEL='95030107755').count() == 0


@pytest.mark.django_db
def test_update_patient_view(client, user):
    patient = Patient.objects.create(first_name='Anna', last_name='Nieznana', PESEL='95030107744')
    assert Patient.objects.get(first_name='Anna', last_name='Nieznana', PESEL='95030107744')
    date_birth = datetime.date.today()
    data = {
        'first_name': 'Anna',
        'last_name': 'Nieznana',
        'PESEL': '95030107744',
        'date_of_birth': date_birth,
        'address': 'address test',
        'contact': 'contact test'
    }
    client.force_login(user)
    response = client.post(f'/patient/update/{patient.pk}/', data)
    patient.refresh_from_db()
    assert response.status_code == 302
    assert Patient.objects.get(address='address test', contact='contact test')


@pytest.mark.django_db
def test_patient_details_view(client, user):
    patient = Patient.objects.create(first_name='Tomek', last_name='Atomek', PESEL='95030107722')
    assert Patient.objects.get(first_name='Tomek', last_name='Atomek', PESEL='95030107722')
    client.force_login(user)
    response = client.get(f'/patient/details/{patient.pk}/')
    assert response.status_code == 200
    assert response.context['patient'] == patient
