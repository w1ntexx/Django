from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import LoginUserForm
from django.views.generic import FormView
from django.urls import reverse_lazy

def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"]
                )
            if user and user.is_active:
                login(request, user)
                return redirect("home")
    else:
        form = LoginUserForm()
    return render(request, "users/login.html", {"form": form})


# class LoginUser(FormView):
#     form_class = LoginUserForm
#     template_name = "users/login.html"
#     success_url = reverse_lazy("home")

#     def form_valid(self, form):
#         cd = form.cleaned_data
#         user = authenticate(
#             request=self.request,
#             username=cd["username"],
#             password=cd["password"],
#         )
#         if user and user.is_active:
#             login(self.request, user)
#             return super().form_valid(form)


def logout_user(request):
    logout(request)
    return redirect("users:login")


        