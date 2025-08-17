from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm

# Optional simple home view
def home_view(request):
    return render(request, 'home.html')

# Register new users
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # password hashed automatically
            messages.success(request, 'Your account was created. You can log in now!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# View/Edit profile (requires login)
@login_required
def profile_view(request):
    profile = request.user.profile  # thanks to OneToOne relation
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})