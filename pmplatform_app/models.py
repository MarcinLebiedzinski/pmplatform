from django.db import models

# Import tabeli domyślnej User (auth_user)
from django.contrib.auth.models import User


# Create your models here.

def get_name(self):
    return '{} {}'.format(self.first_name, self.last_name)


User.add_to_class("__str__", get_name)


class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    set_up_date = models.DateField(auto_now_add=True)
    predicted_finish_date = models.DateField(null=False)
    finish_date = models.DateField(null=True)
    is_finish = models.BooleanField(default=False)
    # Relacja wiele do jednego (many to one) do tabeli User (auth_user)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    set_up_date = models.DateField(auto_now_add=True)
    predicted_finish_date = models.DateField(null=False)
    finish_date = models.DateField(null=True)
    is_finish = models.BooleanField(default=False)
    # relacja wiele do jednego (many to one) do tabeli Project
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    # relacja wiele do wielu (many to many) do tabeli User (auth_user)
    user = models.ManyToManyField(User, through='UserTask')

    def __str__(self):
        return self.name


class UserTask(models.Model):
    date = models.DateField(null=True) # ewentualnie datetime
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    amount_of_time = models.PositiveSmallIntegerField(null=True)
    comment = models.TextField(null=True)


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)

