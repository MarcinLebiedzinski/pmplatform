from django.shortcuts import render, redirect
from django.views import View
from django.views.static import serve
import os


# Create your views here.
class Resume(View):
    def get(self, request):
        ctx = {}
        return render(request, 'resume_eng.html', ctx)


class CvDownload(View):
    def get(self, request):
        filepath = 'resume_app/static/cv_mlebiedzinski.pdf'
        return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
