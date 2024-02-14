from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.db.models.base import Model as Model
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:login")
    
class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {"title": "Профиль пользователя"}
    
    def get_success_url(self):
        return reverse_lazy("users:profile")
    
    def get_object(self):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:password_change_done")

    

    
def logout_user(request):
    logout(request)
    return redirect("users:login")
