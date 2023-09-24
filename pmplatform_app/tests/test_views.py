import pytest


def test_admin_url(client):
    response = client.get('/admin/login/')
    assert response.status_code == 200


def test_submit_url(client):
    response = client.get('/pmplatform/submit/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_main_url(client, user):
    client.login(username='Maciek', password='maciek123!')
    response = client.get('/pmplatform/main/')
    assert response.context['logged_user'] == user
    assert response.status_code == 200


@pytest.mark.django_db
def test_userslist_url(client, users_list):
    client.login(username='Maciek', password='maciek123!')
    response = client.get('/pmplatform/userslist/')
    assert response.status_code == 200
    assert response.context['logged_user'] in users_list
    assert len(response.context['team']) == 3


@pytest.mark.django_db
def test_projectslist_url(client, projects_list):
    client.login(username='Maciek', password='maciek123!')
    response = client.get('/pmplatform/projectslist/')
    assert response.status_code == 200
    assert response.context['logged_user'].username == 'Maciek'
    assert len(response.context['projects']) == 2
    assert response.context['projects'][0].name == 'project_test1'
