from autherization.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from autherization.views import *
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView,View
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from autherization.forms import *
from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.cache import never_cache
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
import logging
from datetime import datetime, timedelta
from django.utils import timezone


# Create your views here.


@login_required
@never_cache
def nurse_panel_view(request):
    return render(request, 'Nurse/nursepanel.html')


def nurse_profile(request):
    # Retrieve the current logged-in user
    current_user = request.user
    
    # Query the Nurse model to get the nurse profile associated with the current user
    try:
        nurse_profile = Nurse.objects.get(user=current_user)


    except Nurse.DoesNotExist:
        # Handle the case where the nurse profile does not exist
        nurse_profile = None
    
    # Pass the nurse profile data to the template context
    context = {
        'nurse_profile': nurse_profile
    }
    
    # Render the template with the provided context
    return render(request, 'Nurse/nurse_profile.html',context)



def remove_profile(request,*args,**kwargs):
   id=kwargs.get("pk")
   Nurse.objects.filter(id=id).delete()
   messages.success(request,"Profile removed")
   return redirect("nursepanel")




from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class NurseProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Nurse
    form_class =NurseProfileUpdateForm
    template_name = 'Nurse/change_profile.html'
    success_url = reverse_lazy('nurse_profile')
    context_object_name="nurse_profile"

    
    def get_object(self, queryset=None):
        return Nurse.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.user.email
        context['name'] = self.request.user.name
        return context
    

    def get_initial(self):
       
        initial = super().get_initial()
        
        user = self.request.user
        initial['email'] = user.email
        

        initial['name'] = user.name  
        
    def form_valid(self, form):
        
        nurse_profile = form.save(commit=False)
        nurse_profile.save()

        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()
        self.request.user.name= form.cleaned_data['name']
        self.request.user.save()


        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update profile")
        return super().form_invalid(form)


class NurseListView(ListView):
    model = Nurse
    template_name = 'Nurse/profile.html'  
    context_object_name = 'nurses'

    def get_queryset(self):
        return Nurse.objects.filter(is_active=True, )
    

# 
    

class NurseDetailView(View):
    def get(self,request,pk):
        nurse_obj = Nurse.objects.get(user__id= pk)
        context = {
            "nurse":nurse_obj
        }
        return render(request,'Nurse/nurseprofile_for_user.html',context)
    



class CreateBookingView(View):
    def get(self, request, pk=None):
        form = BookingForm()
        return render(request, 'Nurse/booking.html', {'form': form})
    
    def post(self, request, pk=None):
        
        form = BookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            duration = form.cleaned_data['duration']
            user = request.user
            nurse = Nurse.objects.get(user__id=pk) if pk else None
            nurse.has_requested = True
            nurse.save()

                
            booking = NurseBooking.objects.create(user=user, nurse=nurse, date=date, duration=duration)
            booking.save()
            messages.success(request, 'Booking successful!')
            return redirect('customerpanel')
            
        return render(request, 'Nurse/booking.html', {'form': form})
    


def bookingsuccess(request):
    return render(request,"Nurse/bookingsuccess.html")


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class NurseUserList(ListView):
    model = NurseBooking
    template_name = 'Nurse/nursepanel.html'
    context_object_name = "nurse_user"

    def get_queryset(self):
    #    nurse=self.request.user
       queryset = super().get_queryset()

       queryset = queryset.filter(nurse=self.request.user.id,is_active=False)
       return queryset

 


def request_approval(request, id):
    bookings = NurseBooking.objects.filter(user_id=id)
    
    for booking in bookings:
        user_name = booking.user.username
        user_email = booking.user.email
        booking.is_active = True
        booking.save()

    # Update nurse availability
    nurse = Nurse.objects.get(user=request.user)
    nurse.is_available = False
    nurse.save()

    # Send email to user
    subject = "Your Home Nurse Request Has Been Approved"
    message = (
        f"Dear {user_name},\n\n"
        "We are pleased to inform you that your request for a home nurse service has been approved!\n\n"
        "At CareLink, we are committed to providing you with the best possible care and support.\n\n"
        "Your assigned nurse will be in touch with you shortly to discuss the details of your care plan.\n\n"
        "Thank you for choosing CareLink. We look forward to assisting you in your journey to better health.\n\n"
        "Best regards,\n"
        "The CareLink Team"
    )
    email_from = "carelink30@gmail.com"
    email_to = user_email
    send_mail(subject, message, email_from, [email_to])

    return redirect('nursepanel')




def nurse_delete(request, id):
    try:
        obj = NormalUser.objects.get(id=id)
        print("Nurse object:", obj)  
        obj.delete()
        print("Nurse profile deleted successfully.") 
        return redirect("index")
    except NormalUser.DoesNotExist:
        print("Nurse profile does not exist.")  
        return redirect("index")



# class ReportCreateView(CreateView):
#     model = Report
#     fields = [ 'details']    

#     template_name = 'Nurse/report.html'
#     success_url = 'nursepanel' 

#     def form_valid(self, form):
#         # form.instance.user = self.request.user
#         return super().form_valid(form)

def list_works(request):
    try:
        works = NurseBooking.objects.filter(nurse__user = request.user).order_by('-created_at')
    
    except NurseBooking.DoesNotExist:
        works = None  
    except Exception as e:

        print(e)
        works = None

    context= {
        "works": works
    }
    return render(request,'Nurse/report.html',context)



def nurse_reports(request, pk):
    # Get the NurseBooking instance
    booking = NurseBooking.objects.get(id=pk)
    reports = Report.objects.filter(user = booking).order_by('-date')

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            # Create a new Report instance
            report = form.save(commit=False)
            report.user = booking
            report.save()
            return redirect('nurse_booking', pk=booking.id) 
    else:
        form = ReportForm()

    context = {
        'form': form,
        'booking': booking,
        'reports':reports
    }
    return render(request, 'Nurse/report_list.html', context)



# class ReportList(ListView):
#     model = Report
#     template_name = 'autherization/view_report.html'
#     context_object_name = "reports"

#     def get_queryset(self):
#     #    nurse=self.request.user
#        queryset = super().get_queryset()

#        queryset = queryset.filter(user=self.request.user.id).order_by('-date')
       
#        return queryset




from django.shortcuts import render, get_object_or_404
from .models import NurseBooking, Report

def report_list(request, pk):
    booking = get_object_or_404(NurseBooking, id=pk)
    reports = Report.objects.filter(user=booking).order_by('-date')
    return render(request, "autherization/view_report.html", {'booking': booking, 'reports': reports})


# def ReportCreate(request):
#     if request.method == "POST":
#         report = ReportForm(request.POST)
#         if report.is_valid():
#             report_detail = report.cleaned_data['details']
            
#             reports = Report.objects.create(details=report_detail)
#             reports.save()    
            
#             return redirect("upload_success")
#         else:
#             return HttpResponse("Oops! Upload failed.")
#     return render(request, "Nurse/report_rough.html")    

