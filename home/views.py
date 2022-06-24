# import email
# from email import message
import email
from django.shortcuts import render, HttpResponse, redirect
from dashboard.models import School
from home.models import Contact
from account.models import Account
from dashboard.models import School
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home/home.html')


def handlesignup(request):
    if request.method=="POST":
        # get the post parameters
        username = request.POST['schoolname']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        regno = request.POST['regno']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #checks for errors
        if Account.objects.filter(username=username).exists():
           messages.warning(request, 'Username already exists!')
           return redirect('/usersignup') 

        if len(username)>30:
            messages.warning(request, "username must be under 10 characters!")
            return redirect('/usersignup')

        if Account.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return redirect('/usersignup')

        if not username.isalnum():
            messages.warning(request, 'Username must only contain alphabets or numbers!')
            return redirect('/usersignup')

        if not contact.isdigit():
            messages.warning(request, 'Contact no. must only contain numbers!')
            return redirect('/usersignup')

        if not address.isalnum():
            messages.warning(request, 'Address must only contain alphabets or numbers!')
            return redirect('/usersignup')

        if not regno.isalnum():
            messages.warning(request, 'Registarion No. must only contain numbers!')
            return redirect('/usersignup')

        if len(pass1) < 6:
            messages.warning(request, 'Password must contain atleast 6 characters')
            return redirect('/usersignup')

        if pass1 != pass2:
            messages.warning('password do not match')
            return redirect('/usersignup')  
     
        myuser = Account.objects.create_user(email, username, pass1)
        myuser.is_school = True
        myuser.registration_no = regno
        myuser.save()

        account = myuser
        school_data = School(name=username, contact=contact, address=address, account=account)
        school_data.save()

        messages.success(request, "Your SPMS account has been successfully created")
        return redirect('/')


    else:
        return HttpResponse("404 not found")

def handlelogin(request):
    if request.method == 'POST':
        loginemail = request.POST['loginemail']
        loginpassword = request.POST['loginpass']


        user = authenticate(email=loginemail, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'logged In Successfully')
            return redirect('/dashboard')
        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect('/userlogin')
    
    return HttpResponse('404-not found')

def userlogin(request):
    return render(request, 'home/userlogin.html')
def usersignup(request):
    return render(request, 'home/usersignup.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()

    return redirect('/')

def forgotpassword(request):
    if request.method == 'POST':
        email           = request.POST['email']
        regno           = request.POST['regno']
        pass1           = request.POST['pass1']
        pass2           = request.POST['pass2']

        if not Account.objects.filter(email=email):
            messages.warning(request, 'Email does not exists')
            return redirect('/userlogin')
        
        if not Account.objects.filter(registration_no=regno):
            messages.warning(request, 'Invalid registration no.')
            return redirect('/userlogin')

        if len(pass1) < 8:
            messages.warning(request, 'Password must contain atleast 8 characters')
            return redirect('/userlogin')

        if pass1 != pass2:
            messages.warning('password do not match')
            return redirect('/userlogin')

        myuser          = Account.objects.get(email=email, registration_no=regno)
        myuser.set_password(pass1)
        myuser.save()
        messages.success(request, 'Password has been changed succesfully')
        return redirect('/userlogin')  
        





#for 404 page
def notfound(request):
    return render(request, '404.html')