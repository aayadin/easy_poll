from django.contrib.auth import views
from django.urls import path

from .views import SignUp

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'signup/',
        SignUp.as_view(),
        name='signup'
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change_form'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
]
