from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpResponse

from .models import Project, Task, UserTask
from django.contrib.auth.models import User

from pmplatform_app.forms import ProjectAddForm, TaskAddForm, AprovingForm, APROVING_CHOICES
from pmplatform_app.forms import AddTimeForm, MyScheduleForm, TaskChoiceForm, UnreportedDaysForm, LoginForm

import pandas as pd

import csv

# Create your views here.
# view - page where you can login to the application
class Submit(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'submit.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return redirect('invalid_data')


# view - page where you can logout
class SignOut(LoginRequiredMixin, View):
    def get(self, request):
        form = AprovingForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'signout.html', ctx)

    def post(self, request):
        form = AprovingForm(request.POST)
        if form.is_valid():
            choice_dict = dict(APROVING_CHOICES)
            choice = choice_dict[int(form.cleaned_data['choice'])]
            if choice == 'yes':
                logout(request)
                return redirect('submit')
            return redirect('main')
        else:
            return redirect('invalid_data')


# view - main page of application
class Main(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'main.html', ctx)


# view - page where you can find contact to author
class Contact(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'contact.html', ctx)


# view - page where you can find basic information about application
class About(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'about.html', ctx)


# view - the page to which you are redirected in case of incorrect data is provided
class InvalidData(View):
    def get(self, request):
        return render(request, 'invaliddata.html')


# view - page which shows list of users (members of project team)
class UsersList(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        ctx = {'team': users,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'userslist.html', ctx)


# view - page where You can create new project (add to db)
class ProjectCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = ProjectAddForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'projectcreate.html', ctx)

    def post(self, request):
        form = ProjectAddForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            predicted_finish_date = form.cleaned_data['predicted_finish_date']
            manager = form.cleaned_data['manager']
            Project.objects.create(name=name,
                                   description=description,
                                   predicted_finish_date=predicted_finish_date,
                                   manager=manager)
            return redirect('projects_list')
        else:
            HttpResponseRedirect('invalid_data')


# view - page which shows list of all projects
class ProjectsList(LoginRequiredMixin, View):
    def get(self, request):
        projects = Project.objects.all()
        ctx = {'projects': projects,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'projectslist.html', ctx)


# view - page which shows details of chosen project
class ProjectDetails(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        manager = User.objects.get(id=project.manager_id)
        ctx = {'project': project,
               'manager': manager,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'projectdetails.html', ctx)


# view - page which shows list of all tasks assigned to chosen project
class TasksList(LoginRequiredMixin, View):
    def get(self, request, project_id):
        tasks = Task.objects.filter(project_id=project_id).order_by("predicted_finish_date")
        project = Project.objects.get(id=project_id)
        ctx = {'tasks': tasks,
               'project': project,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'taskslist.html', ctx)


# view - page where You can create new task (add to db)
class TaskCreate(LoginRequiredMixin, View):
    def get(self, request, project_id):
        form = TaskAddForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'taskcreate.html', ctx)

    def post(self, request, project_id):
        form = TaskAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            predicted_finish_date = form.cleaned_data['predicted_finish_date']
            Task.objects.create(name=name,
                                description=description,
                                predicted_finish_date=predicted_finish_date,
                                project_id=project_id)
            return redirect('tasks_list', project_id=project_id)
        else:
            HttpResponseRedirect('invalid_data')


# view - page where You can delete task from db
class TaskDelete(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.delete_choice'

    def get(self, request, project_id, task_id):
        form = AprovingForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'deletetemplate.html', ctx)

    def post(self, request, project_id, task_id):
        form = AprovingForm(request.POST)
        if form.is_valid():
            choice_dict = dict(APROVING_CHOICES)
            choice = choice_dict[int(form.cleaned_data['choice'])]
            if choice == 'yes':
                t = Task.objects.get(id=task_id)
                t.delete()
            return redirect('tasks_list', project_id=project_id)
        else:
            HttpResponseRedirect('invalid_data')


# view - page which shows details of chosen task
class TaskDetails(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        users = UserTask.objects.filter(task_id=task_id)
        users_list = []
        for user in users:
            if (User.objects.get(id=user.user_id).first_name,
                User.objects.get(id=user.user_id).last_name) not in users_list:
                users_list.append(
                    (User.objects.get(id=user.user_id).first_name, User.objects.get(id=user.user_id).last_name))
        ctx = {'task': task,
               'users_list': users_list,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'taskdetails.html', ctx)


# view - page where You can delete project from db
class ProjectDelete(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.delete_choice'

    def get(self, request, project_id):
        form = AprovingForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'deletetemplate.html', ctx)

    def post(self, request, project_id):
        form = AprovingForm(request.POST)
        if form.is_valid():
            choice_dict = dict(APROVING_CHOICES)
            choice = choice_dict[int(form.cleaned_data['choice'])]
            if choice == 'yes':
                p = Project.objects.get(id=project_id)
                p.delete()
            return redirect('projects_list')
        else:
            HttpResponseRedirect('invalid_data')


# Viev - page where You can see Your time reports between two chosen dates
class MySchedule(LoginRequiredMixin, View):
    def get(self, request):
        form = MyScheduleForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'myscheduleform.html', ctx)

    def post(self, request):
        form = MyScheduleForm(request.POST)
        if form.is_valid():
            user = request.user
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            reports = UserTask.objects.filter(user_id=user.id,
                                              date__gte=start_time,
                                              date__lte=end_time
                                              ).order_by('date')
            reports_list = []
            for report in reports:
                reports_list.append((report.id,
                                     report.date,
                                     Project.objects.get(id=(Task.objects.get(id=report.task_id).project_id)).name,
                                     report.task,
                                     report.amount_of_time))

            ctx = {'reports_list': reports_list,
                   'user': user,
                   'logged_user': request.user,
                   'is_staff': request.user.is_staff}

            return render(request, 'myscheduleresult.html', ctx)
        else:
            HttpResponseRedirect('invalid_data')


# view - page where You can delete You report (daily hours assigned to the project)
class ReportDelete(LoginRequiredMixin, View):
    def get(self, request, report_id):
        form = AprovingForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'deletetemplate.html', ctx)

    def post(self, request, report_id):
        form = AprovingForm(request.POST)
        if form.is_valid():
            choice_dict = dict(APROVING_CHOICES)
            choice = choice_dict[int(form.cleaned_data['choice'])]
            if choice == 'yes':
                r = UserTask.objects.get(id=report_id)
                r.delete()
            return redirect('my_schedule')
        else:
            HttpResponseRedirect('invalid_data')


# view - page where You can see total time spent on each project by all team members
class TotalProjectsTime(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.view_choice'

    def get(self, request):
        projects = Project.objects.all()
        list_of_projects = []
        for project in projects:
            tasks = Task.objects.filter(project_id=project.id)
            hours_of_project = 0
            list_of_tasks = []
            for task in tasks:
                reports = UserTask.objects.filter(task_id=task.id)
                hours_of_task = 0
                for report in reports:
                    hours_of_task += report.amount_of_time
                list_of_tasks.append((task.name, hours_of_task))
                hours_of_project += hours_of_task
            list_of_projects.append((project.name, hours_of_project))
        ctx = {'list_of_projects': list_of_projects,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'totalprojectstime.html', ctx)


# view - page where You can see total time spent on each project task by all team members
class TotalTasksTime(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.view_choice'

    def get(self, request):
        tasks = Task.objects.all()
        list_of_tasks = []
        for task in tasks:
            reports = UserTask.objects.filter(task_id=task.id)
            hours_of_task = 0
            for report in reports:
                hours_of_task += report.amount_of_time
            project = Project.objects.get(id=task.project_id)
            list_of_tasks.append((task.name, hours_of_task, project))
        ctx = {'list_of_tasks': list_of_tasks,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'totaltaskstime.html', ctx)


# view - page where You can see unreported time by team members (list of days)
class UnreportedDays(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.view_choice'

    def get(self, request):
        form = UnreportedDaysForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'unreporteddaysform.html', ctx)

    def post(self, request):
        form = UnreportedDaysForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            dates_list = pd.date_range(start=start_time, end=end_time)
            list_of_unreported_days = []
            for day in dates_list:
                if not UserTask.objects.filter(user_id=user.id, date=day):
                    list_of_unreported_days.append((day.strftime('%Y-%m-%d'), day))
            ctx = {'list_of_unreported_days': list_of_unreported_days,
                   'user': user,
                   'dates_list': dates_list,
                   'start_time': start_time,
                   'logged_user': request.user,
                   'is_staff': request.user.is_staff}
            return render(request, 'unreporteddaysresult.html', ctx)
        else:
            HttpResponseRedirect('invalid_data')


# view - page where You can add time (hours) to task as a daily report - first step (choosing project)
class AddTimeToProject(LoginRequiredMixin, View):
    def get(self, request):
        projects = Project.objects.all()
        ctx = {'projects': projects,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'projects_list_to_add_time.html', ctx)


# view - page where You can add time (hours) to task as a daily report - second step (choosing task)
class AddTimeToTask(LoginRequiredMixin, View):
    login_url = 'submit'

    def get(self, request, project_id):
        tasks = Task.objects.filter(project_id=project_id).order_by("predicted_finish_date")
        project = Project.objects.get(id=project_id)
        ctx = {'tasks': tasks,
               'project': project,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'tasks_list_to_add_time.html', ctx)


# view - page where You can add time (hours) to task as a daily report - third step (fill time form)
class AddTime(LoginRequiredMixin, View):
    def get(self, request, task_id):
        form = AddTimeForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'addtime.html', ctx)

    def post(self, request, task_id):
        form = AddTimeForm(request.POST)
        if form.is_valid():
            task_id = task_id
            user = request.user
            hours = form.cleaned_data['hours']
            comment = form.cleaned_data['comment']
            date = form.cleaned_data['date']
            UserTask.objects.create(task_id=task_id,
                                    user_id=user.id,
                                    amount_of_time=hours,
                                    comment=comment,
                                    date=date)

            return redirect('add_time_to_project')
        else:
            HttpResponseRedirect('invalid_data')


# view - page where You can change status of project as "finished" or "unfinished"
class ChangeProjectStatus(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.view_choice'

    def get(self, request, project_id):
        form = AprovingForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'change_project_status.html', ctx)

    def post(self, request, project_id):
        form = AprovingForm(request.POST)
        if form.is_valid():
            choice_dict = dict(APROVING_CHOICES)
            choice = choice_dict[int(form.cleaned_data['choice'])]
            if choice == 'yes':
                p = Project.objects.get(id=project_id)
                if p.is_finish:
                    p.is_finish = False
                else:
                    p.is_finish = True
                p.save()
            return redirect('add_time_to_project')
        else:
            HttpResponseRedirect('invalid_data')


# view - page where You can change status of task as "finished" or "unfinished"
class ChangeTaskStatus(LoginRequiredMixin, View):
    def get(self, request, task_id):
        form = AprovingForm()
        project = Task.objects.get(id=task_id).project
        ctx = {'form': form,
               'logged_user': request.user,
               'project': project,
               'is_staff': request.user.is_staff}
        return render(request, 'change_task_status.html', ctx)

    def post(self, request, task_id):
        form = AprovingForm(request.POST)
        project = Task.objects.get(id=task_id).project
        if form.is_valid():
            choice_dict = dict(APROVING_CHOICES)
            choice = choice_dict[int(form.cleaned_data['choice'])]
            if choice == 'yes':
                t = Task.objects.get(id=task_id)
                if t.is_finish:
                    t.is_finish = False
                else:
                    t.is_finish = True
                t.save()
            return redirect('add_time_to_task', project.id)
        else:
            HttpResponseRedirect('invalid_data')


# view - page where You can see detailed task report - first step (choosing project)
class TaskReportProjectsList(LoginRequiredMixin, View):
    def get(self, request):
        projects = Project.objects.all()
        ctx = {'projects': projects,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'projects_list_to_task_report.html', ctx)


# view - page where You can see detailed task report - second step (choosing task)
class TaskReportTasksList(LoginRequiredMixin, View):

    def get(self, request, project_id):
        tasks = Task.objects.filter(project_id=project_id).order_by("predicted_finish_date")
        project = Project.objects.get(id=project_id)
        ctx = {'tasks': tasks,
               'project': project,
               'logged_user': request.user,
               'is_staff': request.user.is_staff}
        return render(request, 'tasks_list_to_task_report.html', ctx)


# view - page where You can see detailed task report - third step (report page)
class TaskReport(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.view_choice'

    def get(self, request, task_id):
        reports = UserTask.objects.filter(task_id=task_id).order_by('date')
        task = Task.objects.get(id=task_id)
        reports_list = []
        for report in reports:
            reports_list.append((Project.objects.get(id=task.project_id),
                                 task.name,
                                 User.objects.get(id=report.user_id).first_name,
                                 User.objects.get(id=report.user_id).last_name,
                                 report.date,
                                 report.amount_of_time
                                 ))
        ctx = {'reports_list': reports_list,
               'task': task,
               'logged_user': request.user,
               'project_id': Project.objects.get(id=task.project_id).id,
               'is_staff': request.user.is_staff}
        return render(request, 'taskreport.html', ctx)


class TotalProjectsTimeDownloadCsv(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.view_choice'

    def get(self, request):
        projects = Project.objects.all()
        list_of_projects = []
        for project in projects:
            tasks = Task.objects.filter(project_id=project.id)
            hours_of_project = 0
            list_of_tasks = []
            for task in tasks:
                reports = UserTask.objects.filter(task_id=task.id)
                hours_of_task = 0
                for report in reports:
                    hours_of_task += report.amount_of_time
                list_of_tasks.append((task.name, hours_of_task))
                hours_of_project += hours_of_task
            list_of_projects.append((project.name, hours_of_project))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="totalprojectstime.csv"'

        writer = csv.writer(response)
        for row in list_of_projects:
            writer.writerow(row)
        return response


class TotalTasksTimeDownloadCsv(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'pmplatform_app.view_choice'

    def get(self, request):
        tasks = Task.objects.all()
        list_of_tasks = []
        for task in tasks:
            reports = UserTask.objects.filter(task_id=task.id)
            hours_of_task = 0
            for report in reports:
                hours_of_task += report.amount_of_time
            project = Project.objects.get(id=task.project_id)
            list_of_tasks.append((project, task.name, hours_of_task))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="totaltaskstime.csv"'

        writer = csv.writer(response)
        for row in list_of_tasks:
            writer.writerow(row)

        return response
