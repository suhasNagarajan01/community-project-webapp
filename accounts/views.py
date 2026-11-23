from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .models import User, WorkerProfile, ContractorProfile
from .forms import WorkerRegistrationForm, ContractorRegistrationForm
from jobs.models import Job, JobApplication, Review

def home_view(request):
    """Landing portal with worker vs contractor choice, platform statistics, and top jobs."""
    if request.user.is_authenticated:
        if request.user.is_worker:
            return redirect('worker_dashboard')
        elif request.user.is_contractor:
            return redirect('contractor_dashboard')

    recent_jobs = Job.objects.filter(status='OPEN')[:6]
    stats = {
        'active_jobs': Job.objects.filter(status='OPEN').count() or 42,
        'verified_workers': WorkerProfile.objects.count() or 180,
        'contractors': ContractorProfile.objects.count() or 35,
        'avg_wage': '₹850',
    }
    return render(request, 'home.html', {
        'recent_jobs': recent_jobs,
        'stats': stats,
    })


def login_view(request):
    """Handles both Worker and Contractor login with role selector and demo accounts."""
    if request.user.is_authenticated:
        return redirect('dashboard_router')

    role_tab = request.GET.get('role', 'WORKER')

    if request.method == 'POST':
        action = request.POST.get('action')
        # Instant Demo Login support for frictionless review
        if action == 'demo_worker':
            demo_user = User.objects.filter(role='WORKER').first()
            if demo_user:
                login(request, demo_user)
                messages.success(request, f"Logged in as Worker demo: {demo_user.get_full_name() or demo_user.username}")
                return redirect('worker_dashboard')
        elif action == 'demo_contractor':
            demo_user = User.objects.filter(role='CONTRACTOR').first()
            if demo_user:
                login(request, demo_user)
                messages.success(request, f"Logged in as Contractor demo: {demo_user.get_full_name() or demo_user.username}")
                return redirect('contractor_dashboard')

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard_router')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/login.html', {'role_tab': role_tab})


def register_view(request):
    """Unified register page with Worker / Contractor tabs."""
    if request.user.is_authenticated:
        return redirect('dashboard_router')

    role_tab = request.GET.get('role', 'WORKER').upper()
    if role_tab not in ['WORKER', 'CONTRACTOR']:
        role_tab = 'WORKER'

    worker_form = WorkerRegistrationForm()
    contractor_form = ContractorRegistrationForm()

    if request.method == 'POST':
        submitted_role = request.POST.get('role_type')
        if submitted_role == 'WORKER':
            worker_form = WorkerRegistrationForm(request.POST)
            if worker_form.is_valid():
                user = worker_form.save()
                login(request, user)
                messages.success(request, "Worker account created! Welcome to the daily wage network.")
                return redirect('worker_dashboard')
            role_tab = 'WORKER'
        elif submitted_role == 'CONTRACTOR':
            contractor_form = ContractorRegistrationForm(request.POST)
            if contractor_form.is_valid():
                user = contractor_form.save()
                login(request, user)
                messages.success(request, "Contractor account created! You can now post jobs and hire workers.")
                return redirect('contractor_dashboard')
            role_tab = 'CONTRACTOR'

    return render(request, 'accounts/register.html', {
        'role_tab': role_tab,
        'worker_form': worker_form,
        'contractor_form': contractor_form,
    })


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request, user_id=None):
    """Displays detailed user profile for worker or contractor."""
    target_user = get_object_or_404(User, pk=user_id) if user_id else request.user
    reviews_received = target_user.reviews_received.all().order_by('-created_at')

    worker_profile = getattr(target_user, 'worker_profile', None)
    contractor_profile = getattr(target_user, 'contractor_profile', None)

    return render(request, 'accounts/profile.html', {
        'profile_user': target_user,
        'worker_profile': worker_profile,
        'contractor_profile': contractor_profile,
        'reviews': reviews_received,
        'is_own_profile': target_user == request.user,
    })


@login_required
def profile_edit_view(request):
    """Allows workers and contractors to update bio, phone, locality, skills, and daily wage."""
    user = request.user
    worker_profile = getattr(user, 'worker_profile', None)
    contractor_profile = getattr(user, 'contractor_profile', None)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.locality = request.POST.get('locality', user.locality)
        user.save()

        if user.is_worker and worker_profile:
            worker_profile.skills = request.POST.get('skills', worker_profile.skills)
            worker_profile.languages_known = request.POST.get('languages_known', worker_profile.languages_known)
            worker_profile.expected_daily_wage = request.POST.get('expected_daily_wage', worker_profile.expected_daily_wage)
            worker_profile.bio = request.POST.get('bio', worker_profile.bio)
            worker_profile.availability_status = request.POST.get('availability_status', worker_profile.availability_status)
            worker_profile.save()

        elif user.is_contractor and contractor_profile:
            contractor_profile.company_name = request.POST.get('company_name', contractor_profile.company_name)
            contractor_profile.business_type = request.POST.get('business_type', contractor_profile.business_type)
            contractor_profile.address = request.POST.get('address', contractor_profile.address)
            contractor_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'accounts/profile_edit.html', {
        'worker_profile': worker_profile,
        'contractor_profile': contractor_profile,
    })


@login_required
def settings_view(request):
    """Settings page for appearance theme, dark mode, language, and account info."""
    return render(request, 'accounts/settings.html')


@require_POST
def toggle_theme_api(request):
    """API endpoint to switch between green (Emerald/White) and brown (Warm Earth/Beige) & dark mode."""
    theme = request.POST.get('theme', 'green')
    mode = request.POST.get('mode', 'light')

    if theme not in ['green', 'brown']:
        theme = 'green'
    if mode not in ['light', 'dark']:
        mode = 'light'

    request.session['theme_preference'] = theme
    request.session['color_mode'] = mode

    if request.user.is_authenticated:
        request.user.theme_preference = theme
        request.user.color_mode = mode
        request.user.save(update_fields=['theme_preference', 'color_mode'])

    return JsonResponse({'status': 'ok', 'theme': theme, 'mode': mode})


def about_view(request):
    return render(request, 'pages/about.html')


def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Thank you! Your message has been received. Our community team will get back to you shortly.")
        return redirect('contact')
    return render(request, 'pages/contact.html')
