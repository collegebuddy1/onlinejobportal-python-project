from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from job.models import *
from django.contrib.auth import authenticate,login,logout
from datetime import date
import os
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request,'index.html')


#admin apis
def admin_login(request):
    error = ""

    if request.method == "POST":
        uname = request.POST['uname']
        pwd = request.POST['pwd']

        user = authenticate(username=uname,password=pwd)

        try:

            if user.is_staff:
                login(request,user)
                error = "No"
            
            else:
                error = "Yes"
        except:
            error = "Yes"
    print('......',error)

    d = {'error':error}

    return render(request,'admin_login.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')

    return render(request,'admin_home.html')

def admin_password_change(request):

    error = ""
    if request.method == "POST":
        cpwd = request.POST['cpwd']
        npwd = request.POST['npwd']
       
        try:
            u = User.objects.get(id = request.user.id)
          
            if u.check_password(cpwd):
                u.set_password(npwd)
                u.save()
                error = "No"
            
            else:
                error = "Not"

        except:
             error = "Yes"
         
    d = {'error':error}

    return render(request,'password_change_admin.html',d)



#user apis
def user_login(request):

    error = ""

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pwd']

        user = authenticate(username= email,password=password)

        if user:

            try:
                user1 = StudentUser.objects.get(user=user)
                
                if user1.status == 'Student':

                    login(request,user)
                    error = "No"

                else:
                    error = "Yes"
                
            except:
                error = "Yes"

        else:
            error = "Yes1"
            
    
    d = {'error':error}


    return render(request,'user_login.html',d)

def user_signup(request):

    error = ""

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        image = request.FILES['image']
        email = request.POST['email']
        pwd = request.POST['pwd']
        contact = request.POST['contact']
        gender = request.POST['gender']

        try:
            user = User.objects.create_user(first_name = fname,last_name = lname, username = email, password=pwd)
            StudentUser.objects.create(user=user,image=image,mobile=contact,gender=gender,status='Student')
            error = "No"

        except:
            error = "Yes"

    d = {'error':error}

    return render(request,'user_signup.html',d)

def user_home(request):

    if not request.user.is_authenticated:
        return redirect('/user_login')

    error = ""

    user1 = StudentUser.objects.get(user=request.user)

    try:
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            contact = request.POST['contact']
            gender = request.POST['gender']
            

            user1.user.first_name = fname
            user1.user.last_name = lname
            user1.user.save()
            user1.mobile = contact
            user1.gender = gender
            user1.save()

            
            if len(request.FILES) != 0:
                if len(user1.image) > 0:
                    os.remove(user1.image.path)
                    user1.image = request.FILES['image']
                    user1.save()

            error = "No"

    except:
        error = "Yes"

    d = {'user1':user1,'error':error}

    return render(request, 'user_home.html',d)

def view_users(request):

    user_data = StudentUser.objects.all()

    data = {'user_data':user_data}

    return render(request,'view_users.html',data)

def delete_user(request,pid):

    student = User.objects.get(id=pid)
    student.delete()

    return redirect('/view_users')

def user_password_change(request):

    error = ""
    if request.method == "POST":
        cpwd = request.POST['cpwd']
        npwd = request.POST['npwd']
        
        try:
            u = User.objects.get(id = request.user.id)
            
            if u.check_password(cpwd):
                u.set_password(npwd)
                u.save()
                error = "No"
            
            else:
                error = "Not"

        except:
             error = "Yes"
        
    d = {'error':error}

    return render(request,'password_change_user.html',d)

def latest_jobs(request):

    jd = Job.objects.all().order_by('start_date')

    d = {'jd':jd}

    return render(request,'latest_job.html',d)

def joblist_user(request):

    jd = Job.objects.all()

    d = {'jd':jd}

    return render(request,'joblist_user.html',d)

def single_jobdisplay(request,pid):
     
    if not request.user.is_authenticated:
        messages.info(request, 'Please Login to view complete job details')
        return redirect('/user_login')

    jd = Job.objects.get(id=pid)
    student = StudentUser.objects.get(user=request.user)
    apply = Apply.objects.filter(student=student)

    li = []

    for i in apply:
        li.append(i.job.id)
    

    d = {'jd':jd,'li':li}

    return render(request,'single_jobdisplay.html',d)

def Logout(request):

    logout(request)
    return redirect('/')


def apply(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    msg = ""

    job = Job.objects.get(id=pid)
    user = request.user
    student = StudentUser.objects.get(user=user)
    apply_date = date.today()

    if job.end_date < apply_date:
        msg = "closed"

    elif job.start_date > apply_date:
        msg = "notopen"

    else:
        if request.method == "POST":
            resume = request.FILES['resume']
            Apply.objects.create(job=job,student=student,resume=resume,apply_date=apply_date)
            msg = "good"
            return redirect('single_jobdisplay',pid)

    d = {"msg":msg,'job':job}
        
    return render(request,'resume_upload.html',d)
    


    

#recruiter apis
def recruiter_login(request):

    error = ""

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pwd']

        user = authenticate(username= email,password=password)

        if user:

            try:
                user1 = Recruiter.objects.get(user=user)
                
                if user1.status == 'recruiter' and user1.progress != 'pending':

                    login(request,user)
                    error = "No"

                else:
                    error = "Not"
                
            except:
                error = "Yes"

        else:
            error = "Yes1"
 
    d = {'error':error}

    return render(request,'recruiter_login.html',d)

def recruiter_signup(request):

    error = ""

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        image = request.FILES['image']
        email = request.POST['email']
        pwd = request.POST['pwd']
        contact = request.POST['contact']
        gender = request.POST['gender']
        company = request.POST['company']

        try:
            user = User.objects.create_user(first_name = fname,last_name = lname, username = email, password=pwd)
            Recruiter.objects.create(user=user,image=image,mobile=contact,gender=gender,company= company,progress='pending',status='recruiter')
            error = "No"

        except:
            error = "Yes"

    d = {'error':error}

    return render(request, 'recruiter_signup.html',d)

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('/recruiter_login')
    
    error = ""
    user = request.user
    rec = Recruiter.objects.get(user = user)

    try:
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            contact = request.POST['contact']
            company = request.POST['company']
            gender = request.POST['gender']
            

            rec.user.first_name = fname
            rec.user.last_name = lname
            rec.user.save()
            rec.mobile = contact
            rec.company = company
            rec.gender = gender
            rec.save()

            
            if len(request.FILES) != 0:
                if len(rec.image) > 0:
                    os.remove(rec.image.path)
                    rec.image = request.FILES['image']
                    rec.save()

            error = "No"

    except:
        error = "Yes"
            
    d = {'rec':rec,'error':error}
   

    return render(request, 'recruiter_home.html',d)
        




def pending_recruiters(request):

    user_data = Recruiter.objects.filter(progress="pending")

    data = {'user_data':user_data}

    return render(request, 'pending_recruiters.html',data)

def accepted_recruiters(request):
    user_data = Recruiter.objects.filter(progress="Accepted")

    data = {'user_data':user_data}

    return render(request,'accepted_recruiters.html',data)

def change_status_to_accept(request,pid):
    
    Recruiter.objects.filter(id=pid).update(progress="Accepted")

    return redirect('pending_recruiters')

def rejected_recruiters(request):

    user_data = Recruiter.objects.filter(progress="Rejected")

    data = {'user_data':user_data}

    return render(request,'rejected_recruiters.html',data)

def change_status_to_reject(request,pid):

    Recruiter.objects.filter(id=pid).update(progress="Rejected")

    return redirect('pending_recruiters')

def all_recruiters(request):
    user_data = Recruiter.objects.all()

    data = {'user_data':user_data}

    return render(request,'all_recruiters.html',data)

def delete_recruiter(request,pid):

    recruiter = User.objects.get(id=pid)
    recruiter.delete()

    return redirect('/all_recruiters')


def recruiter_password_change(request):

    error = ""
    if request.method == "POST":
        cpwd = request.POST['cpwd']
        npwd = request.POST['npwd']
        
        try:
            u = User.objects.get(id = request.user.id)
            
            if u.check_password(cpwd):
                u.set_password(npwd)
                u.save()
                error = "No"
            
            else:
                error = "Not"

        except:
             error = "Yes"
        
    d = {'error':error}

    return render(request,'password_change_recruiter.html',d)

def add_job(request):

    error = ""

    if request.method == "POST":
        jtitle = request.POST['jtitle']
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        skills = request.POST['skills']
        experience = request.POST['exp']
        location = request.POST['location']
        salary = request.POST['salary']
        logo = request.FILES['image']
        desc = request.POST['jdesc']
        creation_date = date.today()
        

        print(start_date)
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        

        try:
           job_data = Job.objects.create(recruiter=recruiter,start_date = start_date,end_date=end_date,title=jtitle,salary=salary,image=logo,desc=desc,experience=experience,location=location,skills=skills,creation_date = creation_date)
           error = "No"

        except:
            error = "Yes"

    
    d = {'error':error}

    return render(request,'add_job.html',d)


def job_list(request):

    if not request.user.is_authenticated:
        return redirect('/recruiter_login')
        
    recruiter = Recruiter.objects.get(user=request.user)

    job_data = Job.objects.filter(recruiter=recruiter)

    d = {'job_data':job_data}   
    return render(request, 'job_list.html',d)


def edit_jobdetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('/recruiter_login')

    d = Job.objects.get(id = pid)

    error = ""

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(d.image) > 0:
                os.remove(d.image.path)
            d.image = request.FILES['image']
            d.save()


        jtitle = request.POST['jtitle']
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        skills = request.POST['skills']
        experience = request.POST['exp']
        location = request.POST['location']
        salary = request.POST['salary']
        desc = request.POST['jdesc']
        
        

        d.title = jtitle
        d.skills = skills
        d.experience = experience
        d.location = location
        d.salary = salary
        d.desc = desc

        try:
            d.save()
            error = "No"

        except:
            error = "Yes"

        if start_date:
            try:
                d.start_date = start_date
                d.save()

            except:
                pass

        
        if end_date:
            try:
                d.end_date = end_date
                d.save()

            except:
                pass

    diss = {'d':d,'error':error}

    return render(request,'edit_jobdetails.html',diss)


def candidates_applied(request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')
   

    apply = Apply.objects.all()

    print(apply)
    
    job = Job.objects.all()

    d = {'ap':apply,'job':job}
    return render(request,'candidates_applied.html',d)