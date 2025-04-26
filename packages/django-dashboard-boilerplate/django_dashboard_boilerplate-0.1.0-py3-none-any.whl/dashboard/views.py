from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView
)
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    CustomPasswordResetForm, CustomSetPasswordForm,
    CustomPasswordChangeForm, UserProfileForm
)
from .models import UserProfile


@login_required
def home(request):
    """
    Render the dashboard home page.
    """
    return render(request, 'dashboard/home.html')


def register_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'dashboard/auth/register.html', {'form': form})


def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'dashboard/auth/login.html', {'form': form})


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('dashboard:login')


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view
    """
    template_name = 'dashboard/auth/password_reset.html'
    email_template_name = 'dashboard/auth/password_reset_email.html'
    subject_template_name = 'dashboard/auth/password_reset_subject.txt'
    success_url = reverse_lazy('dashboard:password_reset_done')
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Custom password reset done view
    """
    template_name = 'dashboard/auth/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom password reset confirm view
    """
    template_name = 'dashboard/auth/password_reset_confirm.html'
    success_url = reverse_lazy('dashboard:password_reset_complete')
    form_class = CustomSetPasswordForm


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Custom password reset complete view
    """
    template_name = 'dashboard/auth/password_reset_complete.html'


class CustomPasswordChangeView(PasswordChangeView):
    """
    Custom password change view
    """
    template_name = 'dashboard/auth/password_change.html'
    success_url = reverse_lazy('dashboard:password_change_done')
    form_class = CustomPasswordChangeForm


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    """
    Custom password change done view
    """
    template_name = 'dashboard/auth/password_change_done.html'


@login_required
def profile_view(request):
    """
    User profile view
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'dashboard/auth/profile.html', {'form': form})
