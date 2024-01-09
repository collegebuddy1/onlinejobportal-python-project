from django.contrib import admin

from job.models import *

admin.site.register((StudentUser,Recruiter,Job,Apply))

# Register your models here.
