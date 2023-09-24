from .models import Project, Task, UserTask
from django.contrib import admin

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(UserTask)

