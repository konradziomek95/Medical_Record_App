from django.test import TestCase
import pytest
from med_record_app.models import MedUser, Location


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
    response = client.post('/location/add', data)
    assert response.status_code == 302
    assert Location.objects.get(name='location')


@pytest.mark.django_db
def test_list_of_locations_view(client, locations, user):
    client.force_login(user)
    response = client.get('/location/list')
    locations = Location.objects.all()
    assert locations.count() == 3
    assert response.status_code == 200
    i = 0
    for location in response.context['object_list']:
        obj = locations[i]
        assert location == obj
        i += 1
