from django.urls import path
from .views import *


urlpatterns = [
    path('adminpanel/', admin_panel_view, name="adminpanel"),

    path("device_list/", device_list, name="device_list"),
    path("device_approval/<int:id>/", device_approval, name="device_approval"),
    path("nurse_list/", nurse_list, name="nurse_list"),
    path("nurse_approval/<int:id>/", nurse_approval, name="nurse_approval"),
    path("feedback_list/", FeedbackListView.as_view(), name="feedback_list"),

]