from django.urls import path
from .views import (
    #base,
    font_page,
    home,
    login,
    donor_registration,
    blood_search,
    donor_profile,
    register_user,
    request_blood,
    notifications,
    donation_benefits,
    admin_dashboard,
    
)
#from .views import HomePageView
urlpatterns = [
#path("", HomePageView.as_view(), name="home"),
#path("base/", base, name="base"),
path("font/", font_page, name="font_page"),
path("home/", home, name="home"),
path("register_user/", register_user, name="register_user"),
path("login/", login, name="login"),
path("donor-registration/", donor_registration, name="donor_registration"),
path("blood-search/", blood_search, name="blood_search"),
path("donor_profile/", donor_profile, name="donor_profile"),
path("request-blood/", request_blood, name="request_blood"),
path("notification/", notifications, name="notifications"),
path("donation-benefits/", donation_benefits, name="donation_benefits"),
path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),  


]