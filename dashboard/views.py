from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.contrib import messages
from accounts.models import User, WorkerProfile, ContractorProfile
from jobs.models import Job, JobApplication, WalletTransaction

@login_required
def dashboard_router(request):
    """Directs logged in user to their role-specific dashboard."""
    if request.user.is_worker:
        return redirect('worker_dashboard')
    elif request.user.is_contractor:
        return redirect('contractor_dashboard')
    return redirect('home')


@login_required
def worker_dashboard(request):
    """
    Worker Home Screen:
    - Search bar
    - Nearby recommendations
    - Skill/Category filtering
    - Location filtering
    - Wage badges & distance estimation
    - HTMX live partial update support
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    locality = request.GET.get('locality', '').strip()
    min_wage = request.GET.get('min_wage', '').strip()
    sort_by = request.GET.get('sort', 'newest')

    jobs_qs = Job.objects.filter(status='OPEN')

    if query:
        jobs_qs = jobs_qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(required_skill__icontains=query) |
            Q(location__icontains=query)
        )

    if category:
        jobs_qs = jobs_qs.filter(category=category)

    if locality:
        jobs_qs = jobs_qs.filter(location__icontains=locality)

    if min_wage:
        try:
            jobs_qs = jobs_qs.filter(pay_offered__gte=float(min_wage))
        except ValueError:
            pass

    if sort_by == 'wage_high':
        jobs_qs = jobs_qs.order_by('-pay_offered')
    elif sort_by == 'distance':
        jobs_qs = jobs_qs.order_by('estimated_distance_km')
    else:
        jobs_qs = jobs_qs.order_by('-created_at')

    # Get user's applied job IDs to display applied state
    applied_job_ids = set(
        JobApplication.objects.filter(worker=request.user).values_list('job_id', flat=True)
    )

    context = {
        'jobs': jobs_qs,
        'applied_job_ids': applied_job_ids,
        'query': query,
        'active_category': category,
        'active_locality': locality,
        'categories': Job.CATEGORY_CHOICES,
        'total_jobs_count': jobs_qs.count(),
    }

    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/job_cards.html', context)

    return render(request, 'dashboard/worker_dashboard.html', context)


@login_required
def contractor_dashboard(request):
    """
    Contractor Home Screen:
    - Displays ranked worker cards instead of jobs
    - Ranking logic: ratings, reviews, reliability score, attendance score, completed jobs
    - Skill and location filters
    - HTMX live search support
    - Floating '+' post job button
    """
    query = request.GET.get('q', '').strip()
    skill_filter = request.GET.get('skill', '').strip()
    min_rating = request.GET.get('min_rating', '').strip()
    sort_by = request.GET.get('sort', 'ranking')

    workers_qs = WorkerProfile.objects.select_related('user').all()

    if query:
        workers_qs = workers_qs.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(skills__icontains=query) |
            Q(user__locality__icontains=query)
        )

    if skill_filter:
        workers_qs = workers_qs.filter(skills__icontains=skill_filter)

    if min_rating:
        try:
            workers_qs = workers_qs.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    if sort_by == 'wage_low':
        workers_qs = workers_qs.order_by('expected_daily_wage')
    elif sort_by == 'rating':
        workers_qs = workers_qs.order_by('-rating', '-reliability_score')
    elif sort_by == 'jobs':
        workers_qs = workers_qs.order_by('-completed_jobs_count')
    else:
        # Default smart ranking score
        workers_qs = workers_qs.order_by('-ranking_score', '-rating')

    context = {
        'workers': workers_qs,
        'query': query,
        'active_skill': skill_filter,
        'total_workers_count': workers_qs.count(),
        'popular_skills': ['Electrician', 'Plumber', 'Painter', 'Mason', 'Housekeeping', 'Security', 'General Helper'],
    }

    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/worker_cards.html', context)

    return render(request, 'dashboard/contractor_dashboard.html', context)


@login_required
def worker_wallet_view(request):
    """
    Worker Wallet Screen:
    - Total earnings
    - Pending payments
    - Previous jobs
    - Payment & withdrawal history
    """
    if not request.user.is_worker:
        messages.warning(request, "The wallet section is intended for daily wage workers.")
        return redirect('contractor_dashboard')

    transactions = WalletTransaction.objects.filter(worker=request.user).order_by('-created_at')
    
    total_earned = transactions.filter(transaction_type='EARNING', status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0.00
    pending_amount = transactions.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0.00
    total_withdrawn = transactions.filter(transaction_type='WITHDRAWAL', status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0.00
    available_balance = float(total_earned) - float(total_withdrawn)

    if request.method == 'POST':
        amount = request.POST.get('withdraw_amount')
        try:
            amount = float(amount)
            if 0 < amount <= available_balance:
                WalletTransaction.objects.create(
                    worker=request.user,
                    amount=amount,
                    transaction_type='WITHDRAWAL',
                    status='COMPLETED',
                    description=f"Direct UPI payout to {request.user.phone_number or 'registered account'}"
                )
                messages.success(request, f"Payout of ₹{amount:.2f} initiated successfully to your UPI!")
                return redirect('worker_wallet')
            else:
                messages.error(request, "Invalid withdrawal amount or exceeds available balance.")
        except ValueError:
            messages.error(request, "Please enter a valid numeric amount.")

    return render(request, 'dashboard/wallet.html', {
        'transactions': transactions,
        'total_earned': total_earned,
        'pending_amount': pending_amount,
        'available_balance': max(0.0, available_balance),
    })


@login_required
def worker_applications_view(request):
    """Displays active and completed job applications for the logged in worker."""
    if not request.user.is_worker:
        return redirect('contractor_dashboard')

    applications = JobApplication.objects.filter(worker=request.user).select_related('job', 'job__contractor').order_by('-applied_at')
    return render(request, 'dashboard/worker_applications.html', {
        'applications': applications
    })
