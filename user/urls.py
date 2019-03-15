from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('user_info/', views.user_info, name="user_info"),
    path('register/', views.register, name="register"),
    path('login_for_medal/', views.login_for_medal, name="login_for_medal"),
    path('change_nickname/', views.change_nickname, name="change_nickname"),
    path('bind_email/', views.bind_email, name="bind_email"),
    path('bind_email_code/', views.send_verification_code, name="send_verification_code"),
    path('change_password/', views.change_password, name="change_password"),
    path('forget_password/', views.forget_password, name="forget_password"),
]
