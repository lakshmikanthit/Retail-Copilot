from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Store


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'inventory/auth/login.html')


def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        company = request.POST.get('company', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Validation
        if not username or not email or not password:
            messages.error(request, 'All required fields must be filled.')
            return render(request, 'inventory/auth/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'inventory/auth/register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'inventory/auth/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'inventory/auth/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'inventory/auth/register.html')

        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            # Update the auto-created profile with additional info
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.company = company
            profile.phone = phone
            profile.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')

    return render(request, 'inventory/auth/register.html')


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def user_profile(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_stores = profile.user.stores.all() if hasattr(profile.user, 'stores') else Store.objects.none()

    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.company = request.POST.get('company', '')
        store_id = request.POST.get('default_store')
        if store_id:
            try:
                profile.default_store = Store.objects.get(id=store_id, users=request.user)
            except Store.DoesNotExist:
                pass
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    context = {
        'profile': profile,
        'user_stores': user_stores,
        'all_stores': Store.objects.all(),
    }
    return render(request, 'inventory/auth/profile.html', context)