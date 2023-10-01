"""pmplatform URL Configuration

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pmplatform_app.views import Main, UsersList, Contact, About, InvalidData
from pmplatform_app.views import ProjectCreate, ProjectsList, ProjectDetails, ProjectDelete
from pmplatform_app.views import TaskCreate, TasksList, TaskDelete, TaskDetails
from pmplatform_app.views import MySchedule, ReportDelete
from pmplatform_app.views import TotalProjectsTime, TotalTasksTime, UnreportedDays
from pmplatform_app.views import TaskReport, TaskReportProjectsList, TaskReportTasksList
from pmplatform_app.views import Submit, SignOut
from pmplatform_app.views import AddTimeToProject, AddTimeToTask, AddTime
from pmplatform_app.views import ChangeProjectStatus, ChangeTaskStatus

from resume_app.views import Resume, CvDownload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pmplatform/submit/', Submit.as_view(), name='submit'),
    path('pmplatform/main/', Main.as_view(), name='main'),
    path('pmplatform/contact/', Contact.as_view(), name='contact'),
    path('pmplatform/about/', About.as_view(), name='about'),
    path('pmplatform/userslist/', UsersList.as_view(), name='users_list'),
    path('pmplatform/projectcreate/', ProjectCreate.as_view(), name='project_create'),
    path('pmplatform/invaliddata/', InvalidData.as_view(), name='invalid_data'),
    path('pmplatform/projectslist/', ProjectsList.as_view(), name='projects_list'),
    path('pmplatform/projectdetails/<int:project_id>/', ProjectDetails.as_view(), name='project_details'),
    path('pmplatform/taskslist/<int:project_id>/', TasksList.as_view(), name='tasks_list'),
    path('pmplatform/taskcreate/<int:project_id>/', TaskCreate.as_view(), name='task_create'),
    path('pmplatform/taskdelete/<int:project_id>/<int:task_id>', TaskDelete.as_view(), name='task_delete'),
    path('pmplatform/taskdetails/<int:task_id>/', TaskDetails.as_view(), name='task_details'),
    path('pmplatform/projectdelete/<int:project_id>/', ProjectDelete.as_view(), name='project_delete'),
    path('pmplatform/myschedule/', MySchedule.as_view(), name='my_schedule'),
    path('pmplatform/reportdelete/<int:report_id>/', ReportDelete.as_view(), name='report_delete'),
    path('pmplatform/reports/totalprojectstime/', TotalProjectsTime.as_view(), name='total_projects_time'),
    path('pmplatform/reports/totaltaskstime/', TotalTasksTime.as_view(), name='total_tasks_time'),
    path('pmplatform/reports/unreporteddays/', UnreportedDays.as_view(), name='unreported_days'),
    path('pmplatform/signout/', SignOut.as_view(), name='sign_out'),
    path('pmplatform/addtimetoproject/', AddTimeToProject.as_view(), name='add_time_to_project'),
    path('pmplatform/addtimetotask/<int:project_id>/', AddTimeToTask.as_view(), name='add_time_to_task'),
    path('pmplatform/addtime/<int:task_id>/', AddTime.as_view(), name='add_time'),
    path('pmplatform/changeprojectstatus/<int:project_id>/', ChangeProjectStatus.as_view(), name='change_project_status'),
    path('pmplatform/changetaskstatus/<int:task_id>/', ChangeTaskStatus.as_view(), name='change_task_status'),
    path('pmplatform/taskreportprojectslist/', TaskReportProjectsList.as_view(), name='task_report_projects_list'),
    path('pmplatform/taskreporttaskslist/<int:project_id>/', TaskReportTasksList.as_view(), name='task_report_tasks_list'),
    path('pmplatform/reports/taskreport/<int:task_id>/', TaskReport.as_view(), name='task_report'),


    path('', Resume.as_view(), name='resume'),
    path('resume/', Resume.as_view(), name='resume'),
    path('resume/cv_download', CvDownload.as_view(), name='cv_download'),
]
