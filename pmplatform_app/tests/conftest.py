from pmplatform_app.models import Project, Task
from datetime import datetime
from django.contrib.auth.models import User
import pytest
from django.test import Client


@pytest.fixture
def project():
    user = User.objects.create(username='Maciek',
                               password='maciek123!',
                               first_name='Maciej',
                               last_name='Nowak',
                               email='maciej.nowak@example.com')
    project = Project.objects.create(name="project_test1",
                                     description='opis testowy',
                                     predicted_finish_date=datetime.now(),
                                     is_finish=False,
                                     manager=user)
    return project


@pytest.fixture
def task():
    user = User.objects.create(username='Maciek',
                               password='maciek123!',
                               first_name='Maciej',
                               last_name='Nowak',
                               email='maciej.nowak@example.com')
    project = Project.objects.create(name="project_test1",
                                     description='opis testowy',
                                     predicted_finish_date=datetime.now(),
                                     is_finish=False,
                                     manager=user)
    task = Task.objects.create(name="task_test1",
                               description='opis testowy',
                               predicted_finish_date=datetime.now(),
                               is_finish=False,
                               project=project)
    return task


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    u = User.objects.create_user(username='Maciek',
                                 password='maciek123!',
                                 first_name='Maciej',
                                 last_name='Nowak',
                                 email='maciej.nowak@example.com')
    return u


@pytest.fixture
def users_list():
    u = User.objects.create_user(username='Maciek',
                                 password='maciek123!',
                                 first_name='Maciej',
                                 last_name='Nowak',
                                 email='maciej.nowak@example.com')
    u = User.objects.create_user(username='Piotrek',
                                 password='piotrek123!',
                                 first_name='Piotr',
                                 last_name='Kargul',
                                 email='piotr.kargul@example.com')
    u = User.objects.create_user(username='Janek',
                                 password='janek123!',
                                 first_name='Jan',
                                 last_name='Kowalski',
                                 email='jan.kowalski@example.com')
    users_list = User.objects.all()
    return users_list


@pytest.fixture
def projects_list():
    u = User.objects.create_user(username='Maciek',
                                 password='maciek123!',
                                 first_name='Maciej',
                                 last_name='Nowak',
                                 email='maciej.nowak@example.com')
    p = Project.objects.create(name="project_test1",
                               description='opis testowy 1',
                               predicted_finish_date=datetime.now(),
                               is_finish=False,
                               manager=u)
    p = Project.objects.create(name="project_test2",
                               description='opis testowy 2',
                               predicted_finish_date=datetime.now(),
                               is_finish=False,
                               manager=u)
    projects_list = Project.objects.all()
    return projects_list

