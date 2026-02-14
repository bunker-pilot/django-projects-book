from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("" , include("django.contrib.auth.urls")),
    path("" , views.dashboard , name = "dashboard"),
    path("register/" , views.UserRegisteration.as_view() , name= "register"),
    path("email-verification/<str:uidb64>/<str:token>/" , views.EmailVerification.as_view() , name = "email_verification"),
    path("edit/" , views.Edit.as_view() , name="edit_profile"),
    path("users-list/", views.UserList.as_view() , name = "users_list"),
    path("users/<username>/" , views.UserDetail.as_view(), name = "user_detail")
]   
"""
 #path("login/" , views.UserLogin.as_view() , name ="login")
    #Login/Logout Views
    path("login/" , auth_views.LoginView.as_view() , name = "login"),
    path("logout/" , auth_views.LogoutView.as_view() , name= "logout"),
    
    #Password Change views and urls
    path("password-change/" , auth_views.PasswordChangeView.as_view() , name ="password_change"),
    path("password-change/done" , auth_views.PasswordChangeDoneView.as_view() , name="password_change_done"),
    
    #password reset views and urls
    path("password-reset/" , auth_views.PasswordResetView.as_view() , name="password_reset"),
    path("password-reset/done/" ,auth_views.PasswordResetDoneView.as_view() , name="password_reset_done" ),
    path("password-reset/<uidb64>/<token>/" , auth_views.PasswordResetConfirmView.as_view() , name= "password_reset_confirm") ,
    path("password-reset/complete/" , auth_views.PasswordResetCompleteView.as_view() , name= "password_reset_complete"),
"""