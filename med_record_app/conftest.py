import pytest

from med_record_app.models import MedUser, Location, Patient, MedicalRecord, Reservation, WorkDay


@pytest.fixture
def user():
    user = MedUser.objects.create_user(
        username='test_user',
        first_name="Adam",
        last_name='Składam',
        password='12345',
        email='email@wp.pl',
        profession='1',
        PWZ='12334'

    )
    assert MedUser.objects.get(username='test_user')
    return user


@pytest.fixture
def locations():
    user = MedUser.objects.create_user(
        username='test_user2',
        first_name="Adam",
        last_name='Składam',
        password='12345',
        email='email@wp.pl',
        profession='1',
        PWZ='12334'

    )
    location1 = Location.objects.create(name='name1', address='address1')
    location1.workers_list.add(user)
    location2 = Location.objects.create(name='name2', address='address2')
    location2.workers_list.add(user)
    location3 = Location.objects.create(name='name3', address='address3')
    location3.workers_list.add(user)
    assert Location.objects.get(name='name3')
    return location1, location2, location3
