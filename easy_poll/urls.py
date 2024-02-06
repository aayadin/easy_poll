from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        include('polls.urls', namespace='polls')
    ),
    path(
        'auth/',
        include('users.urls', namespace='users')
    ),
]
