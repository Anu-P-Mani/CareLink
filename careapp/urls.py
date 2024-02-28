from django.urls import path
from .views import *


urlpatterns = [
    path("userreg/", UserRegistration),
    path("adminlog/", adminlogin),
    path("nursereg/", NurseReg),

    path("base/", base),
    path("userreg/", userreg),
    path('nursereg/', nursereg),

]