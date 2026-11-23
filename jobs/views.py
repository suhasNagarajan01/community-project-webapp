from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Avg
from django.http import JsonResponse
from .models import Job, JobApplication, Review, WalletTransaction
from .forms import JobPostForm, ReviewForm
from accounts.models import User, WorkerProfile, ContractorProfile
from notifications.models import Notification
from .utils import analyze_location_for_workers, calculate_distance_between, extract_locality_key

@login_required
def post_job_view(request):
    """Allows contractors to post daily wage opportunities with N-km proximity analysis."""
    if not request.user.is_contractor and not request.user.is_staff:
        messages.error(request, "Only contractor accounts can post jobs.")
        return redirect('home')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.contractor = request.user
            job.save()

            # Analyze location & dispatch priority alerts to nearby workers within radius_km
            analysis = analyze_location_for_workers(job.location, job.radius_km, job.required_skill)
            nearby_workers = analysis['nearby_workers']
            match_timing = job.priority_window_minutes or analysis['match_timing_minutes']

            # Inform nearby workers first via priority notifications
            for w_profile in nearby_workers:
                Notification.objects.create(
                    recipient=w_profile.user,
                    title="⚡ Priority Job Alert (Nearby)",
                    message=f"New {job.title} posted within {job.radius_km} km of {job.location}! You have priority notification for the next {match_timing} minutes.",
                    notification_type='JOB_POSTED',
                    link=f"/jobs/{job.id}/"
                )

            messages.success(
                request,
                f"Job '{job.title}' posted! {len(nearby_workers)} nearby worker(s) within {job.radius_km} km have been alerted first ({match_timing}-min priority window). The application remains open platform-wide for all workers."
            )
            return redirect('contractor_jobs')
    else:
        form = JobPostForm()

    return render(request, 'jobs/post_job.html', {'form': form})


def analyze_location_api(request):
    """
    Live HTMX/Fetch API endpoint to analyze job site location against nearby workers
    and compute match timings based on the user-selected N-km radius.
    """
    location = request.GET.get('location', '').strip()
    radius_km = request.GET.get('radius_km', 5)
    skill = request.GET.get('skill', '').strip()

    try:
        radius_km = float(radius_km)
    except ValueError:
        radius_km = 5.0

    analysis = analyze_location_for_workers(location, radius_km, skill=skill if skill else None)
    detected_locality = extract_locality_key(location).title()

    return JsonResponse({
        'status': 'success',
        'location': location,
        'detected_locality': detected_locality,
        'radius_km': radius_km,
        'nearby_count': analysis['nearby_count'],
        'total_workers': analysis['total_count'],
        'match_timing_minutes': analysis['match_timing_minutes'],
        'message': f"Analyzing '{detected_locality}': {analysis['nearby_count']} worker(s) found within {radius_km} km. They will be alerted first with a {analysis['match_timing_minutes']}-min priority window before broad distribution."
    })


def job_detail_view(request, pk):
    """Detailed view of an individual job posting."""
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    application = None

    if request.user.is_authenticated and request.user.is_worker:
        application = JobApplication.objects.filter(job=job, worker=request.user).first()
        has_applied = application is not None

    contractor_profile = getattr(job.contractor, 'contractor_profile', None)
    contractor_reviews = Review.objects.filter(reviewee=job.contractor, target_role='CONTRACTOR')[:5]

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'application': application,
        'contractor_profile': contractor_profile,
        'contractor_reviews': contractor_reviews,
    })


@login_required
def apply_job_view(request, pk):
    """Allows workers to submit an application / expression of interest for a job."""
    if not request.user.is_worker:
        messages.error(request, "Only workers can apply for daily wage jobs.")
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(Job, pk=pk)

    if job.status != 'OPEN':
        messages.warning(request, "This job is no longer accepting new applications.")
        return redirect('job_detail', pk=pk)

    existing = JobApplication.objects.filter(job=job, worker=request.user).first()
    if existing:
        messages.info(request, "You have already applied for this job.")
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        worker_note = request.POST.get('worker_note', '').strip()
        app = JobApplication.objects.create(
            job=job,
            worker=request.user,
            worker_note=worker_note,
            status='APPLIED'
        )

        # Send notification to Contractor
        Notification.objects.create(
            recipient=job.contractor,
            title="New Worker Application",
            message=f"{request.user.get_full_name() or request.user.username} applied for '{job.title}' ({job.location}).",
            notification_type='JOB_APPLIED',
            link=f"/jobs/contractor/manage/{job.id}/"
        )

        messages.success(request, f"Application submitted for '{job.title}'! The contractor will contact you shortly.")
        return redirect('worker_applications')

    return redirect('job_detail', pk=pk)


@login_required
def contractor_jobs_view(request):
    """Lists all jobs posted by the logged in contractor."""
    if not request.user.is_contractor:
        return redirect('worker_dashboard')

    jobs = Job.objects.filter(contractor=request.user).order_by('-created_at')
    return render(request, 'jobs/contractor_jobs.html', {'jobs': jobs})


@login_required
def contractor_job_applicants_view(request, pk):
    """Contractor inspects applicants for a specific job and can hire / reject / complete them."""
    job = get_object_or_404(Job, pk=pk, contractor=request.user)
    applications = job.applications.select_related('worker', 'worker__worker_profile').all()

    return render(request, 'jobs/contractor_job_applicants.html', {
        'job': job,
        'applications': applications
    })


@login_required
@transaction.atomic
def update_application_status(request, app_id, action):
    """Handles hiring, rejecting, and completing jobs for an applicant."""
    app = get_object_or_404(JobApplication, pk=app_id, job__contractor=request.user)
    job = app.job
    worker = app.worker

    if action == 'accept':
        if app.status == 'ACCEPTED':
            messages.info(request, f"{worker.get_full_name() or worker.username} has already been hired for this assignment.")
            return redirect('contractor_job_applicants', pk=job.id)
        if job.is_filled:
            messages.warning(request, "All required worker positions for this job are already filled.")
            return redirect('contractor_job_applicants', pk=job.id)

        app.status = 'ACCEPTED'
        app.save(update_fields=['status'])
        job.workers_hired += 1
        if job.workers_hired >= job.workers_required:
            job.status = 'IN_PROGRESS'
        job.save(update_fields=['workers_hired', 'status'])

        Notification.objects.create(
            recipient=worker,
            title="Congratulations! You are Hired",
            message=f"Contractor accepted your application for '{job.title}'! Please be ready for start date {job.start_date}.",
            notification_type='JOB_ACCEPTED',
            link=f"/jobs/{job.id}/"
        )
        messages.success(request, f"Hired {worker.get_full_name() or worker.username} for '{job.title}'.")

    elif action == 'reject':
        app.status = 'REJECTED'
        app.save(update_fields=['status'])
        messages.info(request, f"Application for {worker.get_full_name() or worker.username} marked as not selected.")

    elif action == 'complete':
        # Security & Integrity check: prevent duplicate wallet credits or completing un-hired work
        if app.status == 'COMPLETED':
            messages.info(request, "This assignment has already been completed and wages settled.")
            return redirect('create_review', job_id=job.id, reviewee_id=worker.id)

        if app.status != 'ACCEPTED':
            messages.warning(request, "Only workers who have been hired and accepted can be marked completed.")
            return redirect('contractor_job_applicants', pk=job.id)

        app.status = 'COMPLETED'
        app.save(update_fields=['status'])

        # Update worker profile completed count
        worker_profile = getattr(worker, 'worker_profile', None)
        if worker_profile:
            worker_profile.completed_jobs_count += 1
            worker_profile.save(update_fields=['completed_jobs_count'])
            worker_profile.recalculate_ranking()

        # Create wallet earning record with idempotency check
        WalletTransaction.objects.create(
            worker=worker,
            job=job,
            amount=job.pay_offered,
            transaction_type='EARNING',
            status='COMPLETED',
            description=f"Wages for '{job.title}' - Completed on {job.location}"
        )

        Notification.objects.create(
            recipient=worker,
            title="Work Completed & Wages Credited",
            message=f"₹{job.pay_offered} credited to your wallet for '{job.title}'.",
            notification_type='PAYMENT_CREDITED',
            link="/dashboard/worker/wallet/"
        )

        messages.success(request, f"Marked work completed! ₹{job.pay_offered} credited to worker's wallet.")
        return redirect('create_review', job_id=job.id, reviewee_id=worker.id)

    return redirect('contractor_job_applicants', pk=job.id)


@login_required
def create_review_view(request, job_id, reviewee_id):
    """
    Submits ratings & reviews:
    - Contractor rates worker on punctuality, quality, communication, reliability.
    - Worker rates contractor on timely payment, behavior, job accuracy, safety.
    """
    job = get_object_or_404(Job, pk=job_id)
    reviewee = get_object_or_404(User, pk=reviewee_id)

    # Determine reviewer/reviewee role
    if request.user == job.contractor and reviewee.is_worker:
        target_role = 'WORKER'
    elif request.user.is_worker and reviewee == job.contractor:
        target_role = 'CONTRACTOR'
    else:
        messages.error(request, "Invalid review participants.")
        return redirect('dashboard_router')

    # Check if review already exists
    existing_review = Review.objects.filter(job=job, reviewer=request.user, reviewee=reviewee).first()
    if existing_review:
        messages.info(request, "You have already submitted a review for this job.")
        return redirect('user_profile', user_id=reviewee.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.job = job
            review.reviewer = request.user
            review.reviewee = reviewee
            review.target_role = target_role

            if target_role == 'WORKER':
                s1 = int(request.POST.get('punctuality', 5))
                s2 = int(request.POST.get('work_quality', 5))
                s3 = int(request.POST.get('communication', 5))
                s4 = int(request.POST.get('reliability', 5))
                review.punctuality_score = s1
                review.work_quality_score = s2
                review.communication_score = s3
                review.reliability_score = s4
                overall = (s1 + s2 + s3 + s4) / 4.0
            else:
                s1 = int(request.POST.get('timely_payment', 5))
                s2 = int(request.POST.get('behavior', 5))
                s3 = int(request.POST.get('accuracy', 5))
                s4 = int(request.POST.get('safety', 5))
                review.timely_payment_score = s1
                review.professional_behavior_score = s2
                review.job_accuracy_score = s3
                review.safety_conditions_score = s4
                overall = (s1 + s2 + s3 + s4) / 4.0

            review.overall_rating = round(overall, 2)
            review.save()

            # Recalculate reviewee average rating
            all_reviews = Review.objects.filter(reviewee=reviewee)
            avg_rating = all_reviews.aggregate(Avg('overall_rating'))['overall_rating__avg'] or 5.0
            avg_rating = round(avg_rating, 2)

            if target_role == 'WORKER':
                worker_profile = getattr(reviewee, 'worker_profile', None)
                if worker_profile:
                    worker_profile.rating = avg_rating
                    worker_profile.total_ratings_count = all_reviews.count()
                    worker_profile.save()
                    worker_profile.recalculate_ranking()
            else:
                contractor_profile = getattr(reviewee, 'contractor_profile', None)
                if contractor_profile:
                    contractor_profile.rating = avg_rating
                    contractor_profile.total_ratings_count = all_reviews.count()
                    contractor_profile.save()

            Notification.objects.create(
                recipient=reviewee,
                title="New Review Received",
                message=f"{request.user.get_full_name() or request.user.username} gave you a {review.overall_rating}★ rating for '{job.title}'.",
                notification_type='REVIEW_RECEIVED',
                link=f"/accounts/profile/{reviewee.id}/"
            )

            messages.success(request, "Review submitted successfully! Thank you for strengthening community trust.")
            return redirect('user_profile', user_id=reviewee.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {
        'form': form,
        'job': job,
        'reviewee': reviewee,
        'target_role': target_role,
    })
