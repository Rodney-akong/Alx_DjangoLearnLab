from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from .forms import RegisterForm, UserUpdateForm, ProfileForm

class MyLoginView(LoginView):
    template_name = "accounts/login.html"

class MyLogoutView(LogoutView):
    template_name = "accounts/logout.html"

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # password hashed by UserCreationForm
            login(request, user)
            messages.success(request, "Welcome! Your account was created.")
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/profile.html", context)
