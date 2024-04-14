from django.urls import path
from .views import *

urlpatterns = [
    path('signup/customer/', customer_signup, name='customer_signup'),
    path('signup/nurse/', nurse_signup, name='nurse_signup'),
    path('signup/shop/', shop_signup, name='shop_signup'),
    path('login/', login_view, name='login'),
    path('customerpanel/', customer_panel_view, name='customerpanel'),
    
    
    
    
    path('base/', base),
    path('base2/', base2),
    path('', index, name="index"),
    path('admin_login/', admin_login, name="admin_login"),

    path('forgot/', forgot_password, name="forgot_password"),
    path('reset/', reset_password, name="reset_password"),
    path('change_password/<int:id>', change_password, name="change_password"),

    path('logout/', logout_view.as_view(), name="logout_view"),
    path('aboutus/', aboutus, name='aboutus'),
    path('customer_profile/', customer_profile, name="customer_profile"),
    path("customer_update/<int:id>/", customer_update, name="customer_update"),
    path("add_feedback", add_feedback, name="add_feedback"),
    path("feedback_list/", feedback_list, name="feedback_list"),
    path("feedback_list_index/", feedback_list_index, name="feedback_list_index"),




]