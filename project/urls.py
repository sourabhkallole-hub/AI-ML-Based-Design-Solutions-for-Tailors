"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [

    path("admin_master/", views.adminMaster, name="home"),
    path("admin_history/", views.adminHistory, name="home"),
    path("admin_users/", views.adminReport, name="home"),
    path("admin_contact/", views.adminContact, name="home"),
    path("admin_profile/", views.adminProfile, name="home"),
    path("tailor_profile/", views.tailorProfile, name="home"),

    path("admin_details/", views.adminDetails, name="home"),
    path("admin_history_details/", views.adminHistoryDetails, name="home"),
    path("admin_history_details_individual/", views.adminHistoryIndividualDetails, name="home"),
    path("admin_user_details/", views.adminUserDetails, name="home"),
    path("admin_contact_details/", views.adminContactDetails, name="home"),
    path("get_admin_profile/", views.adminProfileDetails, name="home"),
    path("admin_update_profile/", views.adminUpdateProfileDetails, name="home"),
    path("admin_login/", views.adminLogout, name=""),
    path("admin_logout/", views.adminLogout, name=""),
    path("login_admin/", views.loginAdmin, name="web"),

    path("my_bookings/", views.my_bookings, name="web"),
    path("get_bookings/", views.get_bookings, name="get_bookings"),
    path("update_status/", views.update_status, name="update_status"),
    path("booking_details/<int:bk_id>/", views.get_booking_details, name="booking_details"),

    path("tailor_bookings/", views.tailor_bookings, name="web"),
    path("get_tailor_bookings/", views.get_tailor_bookings, name="get_tailor_bookings"),

    path("admin_design/", views.adminDesign, name="home"),
    path("admin_design_details/", views.adminDesignDetails, name="home"),
    path("admin_design_details_create/", views.adminDesignDetailsCreate, name="home"),
    path("get_designs/", views.getDesigns, name="home"),
    path("save_selected_designs/", views.save_selected_designs, name="save_selected_designs"),

    path("index/", views.webIndex, name="web"),
    path("about/", views.about, name="web"),
    path("contact/", views.contact, name="web"),
    path("", views.loginUser, name="web"),
    path("register/", views.register, name="web"),
    path("profile/", views.profile, name="web"),
    path("web_login/", views.webLogin, name="web"),
    path("web_logout/", views.webLogout, name=""),
    path("add_register/", views.newRegister, name="home"),
    path("save_contact/", views.saveContact, name="home"),
    path("predict/", views.predict, name='predict'),

]
