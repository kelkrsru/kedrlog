from django.contrib.auth import views as auth_views

from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .forms import CreationForm, PasswordResetFormValidation
from core.models import Company


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('accounts:signup_complete')
    template_name = 'users/signup.html'
    extra_context = {'company': get_object_or_404(Company, active=True)}


def signup_complete(request):
    template = 'users/signup_complete.html'
    return render(request, template, {'company': get_object_or_404(Company, active=True)})


class Login(auth_views.LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('personal:index')
    redirect_authenticated_user = True
    extra_context = {'company': get_object_or_404(Company, active=True)}


class Logout(auth_views.LogoutView):
    template_name = 'users/logout.html'
    extra_context = {'company': get_object_or_404(Company, active=True)}


class PasswordReset(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    extra_context = {'company': get_object_or_404(Company, active=True)}
    form_class = PasswordResetFormValidation


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    extra_context = {'company': get_object_or_404(Company, active=True)}


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    extra_context = {'company': get_object_or_404(Company, active=True)}


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    extra_context = {'company': get_object_or_404(Company, active=True)}
