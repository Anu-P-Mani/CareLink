from django.shortcuts import render, redirect
from .forms import *
from medicines.views import *
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.views import View
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from nurse.models import *
from django.utils.crypto import get_random_string



# Create your views here.


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            em = request.POST.get('email')
            form.save()
            subject = "Welcome to CareLink!"
            message = (
                f"Dear Customer,\n\n"
                "Thank you for creating an account with CareLink! "
                "We're thrilled to have you on board.\n\n"
                "Feel free to explore our website and discover a world of exciting products and services tailored just for you.\n\n"
                "If you have any questions or need assistance, don't hesitate to reach out to us.\n\n"
                "Best regards,\n"
                "The CareLink Team"
            )
            email_from = "carelink30@gmail.com"
            email_to = em
            send_mail(subject, message, email_from, [email_to])
            return redirect('login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'autherization/customer_signup.html', {'form': form})

def nurse_signup(request):
    if request.method == 'POST':
        form = NurseSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            em = request.POST.get('email')
            form.save()
            subject = "Welcome to CareLink!"
            message = (
                f"Dear Customer,\n\n"
                "Thank you for creating an account with CareLink! "
                "We're thrilled to have you on board.\n\n"
                "Feel free to explore our website and discover a world of exciting products and services tailored just for you.\n\n"
                "If you have any questions or need assistance, don't hesitate to reach out to us.\n\n"
                "Best regards,\n"
                "The CareLink Team"
            )
            email_from = "carelink30@gmail.com"
            email_to = em
            send_mail(subject, message, email_from, [email_to])
            return redirect('login')
    else:
        form = NurseSignUpForm()
    return render(request, 'autherization/nurse_signup.html', {'form': form})

def shop_signup(request):
    if request.method == 'POST':
        form = ShopSignUpForm(request.POST)
        if form.is_valid():
            em = request.POST.get('email')
            form.save()
            subject = "Welcome to CareLink!"
            message = (
                f"Dear Customer,\n\n"
                "Thank you for creating an account with CareLink! "
                "We're thrilled to have you on board.\n\n"
                "Feel free to explore our website and discover a world of exciting products and services tailored just for you.\n\n"
                "If you have any questions or need assistance, don't hesitate to reach out to us.\n\n"
                "Best regards,\n"
                "The CareLink Team"
            )
            email_from = "carelink30@gmail.com"
            email_to = em
            send_mail(subject, message, email_from, [email_to])
            return redirect('login')
    else:
        form = ShopSignUpForm()
    return render(request, 'autherization/shop_signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_nurse:
                    return redirect('nursepanel')
                elif user.is_customer:
                    return redirect('customerpanel')
                elif user.is_shop:
                    return redirect('shoppanel')
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Form is not valid. Please try again.')
    else:
        form = AdminForm()
    
    return render(request, 'autherization/login.html', {'form': form})
def base(request):
    return render(request, "base.html")


def base2(request):
    return render(request, "base2.html")


def index(request):
    feedbacks = Feedback.objects.all()[::-1][:4]
    medicines = Medicine_inventory.objects.all()[:6]
    devices = DeviceInformation.objects.all()[:4]
    return render(request, "autherization/index.html", {'feedbacks': feedbacks, 'medicines': medicines, 'devices': devices}) 


@login_required
@never_cache
def customer_panel_view(request):
    feedbacks = Feedback.objects.all()[::-1][:4]
    medicines = Medicine_inventory.objects.all()[:6]
    devices = DeviceInformation.objects.all()[:4]

    return render(request, "autherization/customerpanel.html", {'feedbacks': feedbacks, 'medicines': medicines, 'devices': devices})




def admin_login(request):
    if request.method == "POST":
        a = AdminForm(request.POST)
        if a.is_valid():
            unm = a.cleaned_data['username']
            ps = a.cleaned_data['password']
            user = authenticate(request, username=unm, password=ps)
            if user is not None:
                login(request,user)
                return redirect("adminpanel")
            else: 
                return HttpResponse("login failed!")
    return render(request, "autherization/admin_login.html")






def forgot_password(request):
    user_list = NormalUser.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
       
        for user in user_list:
            if user.email == email and user.username == username:
                user_id = user.id
                otp = get_random_string(length=6, allowed_chars='1234567890')
                request.session['otp'] = otp
                subject = "Password reset"
                message = f"Hi {username},\n\nSomeone has requested a new password for the following account on CareLink.\nIf you didn't make this request, please ignore this email.\nTo reset your password, please use the following OTP (One-Time Password): {otp}.\n\nThanks for using CareLink."
                email_from = "carelink30@gmail.com"
                email_to = email
                send_mail(subject, message, email_from, [email_to])
                return redirect('change_password', user_id)
        else:
            return HttpResponse("Oops somthing went wrong !")
    return render(request, "autherization/forgot_password.html")




def change_password(request, id):
    user = NormalUser.objects.get(id=id)
    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp == request.session['otp']:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return redirect("login")
            
            else:
                msg = 'Sorry something went wrong!'
                return render(request, 'autherization/success.html', {'msg': msg})
        else:
            msg = "otp doesn't match!"
            return render(request, 'autherization/success.html', {'msg': msg})   
    return render(request, "autherization/change_password.html")




class logout_view(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(login_view)



def aboutus(request):
    return render(request, "autherization/about.html")


def customer_profile(request):
    current_user = request.user
    
    try:
        customer_profile =  Customer.objects.get(user=current_user)
        
    except Customer.DoesNotExist:
        customer_profile = None
        print("Shop profile does not exist for user:", current_user)
    
    context = {
        'customer_profile': customer_profile
    }
    
    return render(request, 'autherization/customer_profile.html', context)


def customer_update(request, id):
    customer = Customer.objects.get(user_id=id)
    
    
    form = LoginForm(instance=customer)
    
    if request.method == "POST":
        form = LoginForm(request.POST, instance=customer)
        if form.is_valid():
            form.username = request.POST.get('username')
            form.email = request.POST.get('email')
            form.phone = request.POST.get('phone')
            form.address = request.POST.get('address')



            form.save()
            return redirect('customer_profile' )
    
    return render(request, "autherization/customer_update.html", {'form': form})




def add_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            user = request.user
            feedback = Feedback.objects.create(user=user, comment=comment)
            feedback.save()
            return redirect('feedback_success')  # Redirect to a success page
    else:
        form = FeedbackForm()

    return render(request, 'autherization/add_feedback.html', {'form': form})


class FeedBackSuccess(TemplateView):
    template_name = "autherization/feedback_success.html"
        
 

 