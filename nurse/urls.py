from django.urls import path,include
from nurse.views import *
from autherization.urls import *
urlpatterns = [

    path('Nurse/nurse_profile/', nurse_profile, name="nurse_profile"),
    path("Nurse/remove/", remove_profile, name='removeprofile'),
    path("change/<int:pk>/",NurseProfileUpdateView.as_view(),name="changeprofile"),
    path("Nurse/approved_nurses/",NurseListView.as_view(),name="approved_nurses_list"),

    path("Nurse/approved_nurse_profile/<int:pk>",NurseDetailView.as_view(),name="approved_nurse_profile"),
    path("Nurse/booking/<int:pk>", CreateBookingView.as_view(), name="booking"),
    path("Nurse/bookingsuccess/", bookingsuccess, name="bookingsucces"),
    path("Nurse/nursepanel/", NurseUserList.as_view(), name="nursepanel"),
    path("Nurse/user_approval/<int:id>/", request_approval, name="user_approval"),
    path('Nurse/update/<int:pk>', NurseProfileUpdateView.as_view() , name="changeprofile"),
    path('nurse/delete/<int:id>', nurse_delete, name='delete_nurse_profile'),
    path('report/', list_works, name="report"),
    path('nurse/work/report/<int:pk>',nurse_reports,name='nurse_booking'),

    path('report_for_user/', reports, name="report_for_user"),
    path("view_report/<int:pk>", report_list, name="view_report"),



    ]