from django.shortcuts import render,redirect, get_object_or_404
from nurse.forms import *
from clinical_devices.models import *
from django.core.mail import send_mail
from django.conf import settings
from autherization.models import *
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView,View
from nurse.models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


# Create your views here.

def device_list(request):
    device = DeviceInformation.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, "admin/device_list.html", {'device_list': device})



def device_approval(request, id):

    device = DeviceInformation.objects.get(id=id) 
    user_name = device.user.username
    user_email = device.user.email
    device.is_approved=True
    device.save()
    subject = "Approval Confirmation"
    message = (
        f"Hi {user_name},\n\n"
        "Congratulations! Your device upload request has been approved. "
        "You can now access and manage your device.\n\n"
        "Thank you for choosing us.\n\n"
        "Best regards,\n"
        "CareLink"
    )
    email_from = "carelink30@gmail.com"
    email_to = user_email
    send_mail(subject, message, email_from, [email_to])

    return redirect('device_list')


def nurse_list(request):
    nurse = Nurse.objects.filter(is_active=False)
    return render(request, "admin/nurselist.html", {'nurse_list': nurse})


def nurse_approval(request,id):
    nurse = Nurse.objects.get(user_id=id) 
    user_name = nurse.user.username
    user_email = nurse.user.email
    nurse.is_active=True
    nurse.save()
    subject = "Welcome to the CareLink Family!"
    message = (
        f"Dear {user_name},\n\n"
        "We are thrilled to welcome you to the CareLink family! Your request has been approved, and you are now an integral part of our team.\n\n"
        "At CareLink, we value your commitment to providing exceptional care and support. Your dedication is truly appreciated.\n\n"
        "Thank you for choosing CareLink. We look forward to working together to make a positive impact on the lives of those we serve.\n\n"
        "Best regards,\n"
        "The CareLink Team"
    )
    email_from = "carelink30@gmail.com"
    email_to = user_email
    send_mail(subject, message, email_from, [email_to])
    return redirect('nurse_list')



@login_required
@never_cache
def admin_panel_view(request):
    nurses = NurseBooking.objects.filter(is_active=True)

    return render(request, "admin/admin_panel.html", {'nurses': nurses})


class FeedbackListView(ListView):
    model = Feedback
    template_name = "admin/feedback_list.html"
    context_object_name = 'feedbacks'

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

def delete_nurse(request, pk):
    nurse= get_object_or_404(Nurse, pk=pk)
    nurse.delete()
    return redirect('nurse_list')

class Listapprovednurse(ListView):
    model = Nurse
    template_name = 'admin/approvednurse.html'  
    context_object_name = 'nurses'

    def get_queryset(self):
        return Nurse.objects.filter(is_active=True)
    


