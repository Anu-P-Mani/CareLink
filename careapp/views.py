from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import HttpResponse
from django.core import validators
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
 
    
def UserRegistration(request):
    if request.method == "POST":
        a = UserForm(request.POST)
        if a.is_valid():
            u_name = a.cleaned_data['username']
            em = a.cleaned_data['email']
            ph = a.cleaned_data['phone']
            addr = a.cleaned_data['address']
            pwd = a.cleaned_data['password']
            cpwd = a.cleaned_data['cpassword']
            
                
            #     # Password validation
            # errors = []
            # if len(pwd) < 8:
            #     errors.append("Password must be at least 8 characters long.")
            # if not any(char.isupper() for char in pwd):
            #     errors.append("Password must contain at least one uppercase letter.")
            # if not any(char in "!@#$%^&*()-_+={}[]:;\"'<>,.?/~" for char in pwd):
            #     errors.append("Password must contain at least one special character.")
            # if pwd != cpwd:
            #     errors.append("Passwords do not match.")
            # else:
            if pwd == cpwd:
                b = UserRegistration(username=u_name,email=em,phone=ph,address=addr,password=pwd)
                b.save()    
                subject = "Your account has been created"
                message = f"Your username is {u_name}"
                email_from = "bankprj95@gmail.com"
                email_to = em
                send_mail(subject, message, email_from, [email_to])

            
                return HttpResponse("reg success")
            else:
                return HttpResponse("password doesn't match")  
        else:
            return HttpResponse("reg failed")          
    return render(request, "userRegistration.html")


# def register(request):
#     if request.method == "POST":
#         u = request.POST['u']
#         p = request.POST['p']
#         p1 = request.POST['p1']
#         e = request.POST['e']
#         f = request.POST['f']
#         l = request.POST['l']

#         # Password validation
#         errors = []
#         if len(p) < 8:
#             errors.append("Password must be at least 8 characters long.")
#         if not any(char.isupper() for char in p):
#             errors.append("Password must contain at least one uppercase letter.")
#         if not any(char in "!@#$%^&*()-_+={}[]:;\"'<>,.?/~" for char in p):
#             errors.append("Password must contain at least one special character.")
#         if p != p1:
#             errors.append("Passwords do not match.")

#         # Email validation
#         try:
#             validate_email(e)
#         except ValidationError:
#             errors.append("Invalid email address.")

#         if errors:
#             error_message = "\n".join(errors)
#             messages.error(request, error_message)
#             return redirect('UserAuthentication:register')  # Redirect back to registration form with error messages

#         try:
#             # If no errors, create the user
#             user = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)

#             # Send confirmation email
#             subject = 'Registration Successful'
#             message = f"Hello {u},\n\nThank you for registering with us. Your account has been successfully created.\n\nYou can now login to your account."
#             from_email = 'sreeragp10@gmail.com'  # Update with your Gmail address
#             to_email = [e]  # Use the provided email address
#             send_mail(subject, message, from_email, to_email)

#             # Registration successful message
#             messages.success(request, "Registration successful. You can now login.")
#             return redirect('UserAuthentication:login')

#         except IntegrityError:
#             messages.error(request, "Username or email address already exists.")
#             return redirect('UserAuthentication:register')  # Redirect back to registration form with error message

#     return render(request, 'userAuth/register.html')


def NurseReg(request):
    return render(request, "NurseRegistration.html"
                  )


def adminlogin(request):
    if request.method == "POST":
        a = adminform(request.POST)
        if a.is_valid():
            us = a.cleaned_data['username']
            ps = a.cleaned_data['password']
            user = authenticate(request, username=us, password=ps)
            if user is not None:
                # return redirect(adminindex)
                return HttpResponse("success")
            else:
                return HttpResponse("Login failed")
    return render(request, "adminlogin.html")


def base(request):
    return render(request, "base.html")

def userreg(request):
    return render(request, "UserRegistration.html")

def nursereg(request):
    return render(request, "NurseRegistration.html")