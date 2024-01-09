"""onlinejobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from job.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('admin_login/',admin_login,name="admin_login"),
    path('admin_home/',admin_home,name="admin_home"),
    path('admin_password_change/',admin_password_change,name="admin_password_change"),
    

    path('user_login/',user_login,name="user_login"),
    path('user_signup/',user_signup,name="user_signup"),
    path('user_home/',user_home,name="user_home"),
    path('view_users/',view_users,name="view_users"),
    path('delete_user/<int:pid>',delete_user,name="delete_user"),
    path('user_password_change/',user_password_change,name="user_password_change"),
    path('latest_jobs',latest_jobs,name="latest_jobs"),
    path('single_jobdisplay/<int:pid>',single_jobdisplay,name="single_jobdisplay"),
    path('joblist_user/',joblist_user,name="joblist_user"),
    path('apply/<int:pid>',apply,name="apply"),
    path('resume_upload/<int:pid>',apply,name="resume_upload"),
    path('candidates_applied',candidates_applied,name="candidates_applied"),

    

    path('recruiter_login/',recruiter_login,name="recruiter_login"),
    path('recruiter_signup/',recruiter_signup,name="recruiter_signup"),
    path('recruiter_home/',recruiter_home,name="recruiter_home"),
    path('pending_recruiters',pending_recruiters,name="pending_recruiters"),
    path('accept_user/<int:pid>',change_status_to_accept,name="accept_user"),
    path('accepted_recruiters',accepted_recruiters,name="accepted_recruiters"),
    path('rejected_recruiters',rejected_recruiters,name="rejected_recruiters"),
    path('reject_user/<int:pid>',change_status_to_reject,name="reject_user"),
    path('all_recruiters',all_recruiters,name="all_recruiters"),
    path('delete_recruiter/<int:pid>',delete_recruiter,name="delete_recruiter"),
    path('recruiter_password_change/',recruiter_password_change,name="recruiter_password_change"),
    path('add_job/',add_job,name="add_job"),
    path('job_list/',job_list,name="job_list"),
    path('edit_jobdetails/<int:pid>',edit_jobdetails,name="edit_jobdetails"),


    path('Logout/',Logout,name="Logout"),
    
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
