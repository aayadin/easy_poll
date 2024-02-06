from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class: CreationForm = CreationForm
    success_url: str = reverse_lazy('posts:index')
    template_name: str = 'users/signup.html'


class PasswordChangeView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
