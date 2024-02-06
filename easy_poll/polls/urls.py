from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'poll/<int:id>',
        views.poll,
        name='poll'
    ),
]
