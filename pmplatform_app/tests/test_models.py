from pmplatform_app.models import Project, User, Task
import pytest


@pytest.mark.django_db
def test_project_model(project):
    assert len(Project.objects.all()) == 1
    assert Project.objects.get(name='project_test1') == project


@pytest.mark.django_db
def test_project_task(task):
    assert len(Task.objects.all()) == 1
    assert Task.objects.get(name='task_test1') == task
