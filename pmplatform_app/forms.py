from django import forms
from django.forms import TextInput, PasswordInput
from pmplatform_app.models import Project, Task, UserTask, UserDetails
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta


class ProjectAddForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Project name', max_length=64)
    description = forms.CharField(label='Project description',
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    predicted_finish_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-group'}),
                                            initial=datetime.now())
    manager = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'),
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     label='Responsible person')


class TaskAddForm(forms.Form):
    name = forms.CharField(label='Task name', max_length=64,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Project description',
                                  widget=forms.Textarea(attrs={'class': 'form-control'}),
                                  required=False)
    predicted_finish_date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.now())


APROVING_CHOICES = (
        (1, "yes"),
        (2, "no"),
    )


class AprovingForm(forms.Form):
    choice = forms.ChoiceField(choices=APROVING_CHOICES, initial=1, label="Are You sure?")


class AddTimeForm(forms.Form):
    # user = forms.ModelChoiceField(queryset=User.objects.all()) - dana pobierana z sesji
    hours = forms.IntegerField(label='hours', min_value=0, max_value=8)
    comment = forms.CharField(label='Comment',
                              widget=forms.Textarea(attrs={'class': 'form-control'}),
                              required=False)
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.now())


class MyScheduleForm(forms.Form):
    # user = forms.ModelChoiceField(queryset=User.objects.all()) - dana pobierana z sesji
    start_time = forms.DateField(label='start time', widget=forms.SelectDateWidget,
                                 initial=(datetime.now()-timedelta(days=30)))
    end_time = forms.DateField(label='end time', widget=forms.SelectDateWidget, initial=datetime.now())


class TaskChoiceForm(forms.Form):
    task = forms.ModelChoiceField(queryset=Task.objects.all())


class UnreportedDaysForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    start_time = forms.DateField(label='start time', widget=forms.SelectDateWidget,
                                 initial=(datetime.now()-timedelta(days=30)))
    end_time = forms.DateField(label='end time', widget=forms.SelectDateWidget, initial=datetime.now())


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='username', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='password')