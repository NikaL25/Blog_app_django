from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import UserRegisterForm, ProfileForm
from blogs.models import Notification
from .models import Profile
from django.contrib.auth.models import User
from django.db.models import Q


def user_login(request):
    if request.method == 'POST':
        identifier = request.POST['username']
        password = request.POST['password']

        print("=== DEBUG ===")
        print("Entered:", identifier)
        print("Password:", password)

        try:
            user_obj = User.objects.get(
                Q(username=identifier) | Q(email=identifier))
            user = authenticate(
                request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('blogs:blog_list')
        else:
            print("Authentication failed")

        return render(request, 'blogs/blog_list.html', {'error': 'Incorrect'})

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('accounts:login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def user_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("For administrators only")
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("For administrators only")
    user = User.objects.get(id=user_id)
    if user != request.user:
        user.delete()
    return redirect('accounts:user_list')


@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('accounts:login')
    return render(request, 'accounts/delete_profile.html')


@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user).order_by('-created_at')
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifications': notifications})


@login_required
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id, recipient=request.user)
        notification.delete()
        return redirect('accounts:notifications')
    except Notification.DoesNotExist:
        return HttpResponseForbidden("The notification was not found or does not belong to you.")
