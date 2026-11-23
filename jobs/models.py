from django.db import models
from django.conf import settings
from django.utils import timezone

class Job(models.Model):
    CATEGORY_CHOICES = (
        ('CONSTRUCTION', 'Construction & Masonry'),
        ('PLUMBING', 'Plumbing & Pipe Fitting'),
        ('ELECTRICAL', 'Electrical Work'),
        ('PAINTING', 'Painting & Whitewashing'),
        ('CARPENTRY', 'Carpentry & Woodwork'),
        ('HOUSEKEEPING', 'Housekeeping & Deep Cleaning'),
        ('SECURITY', 'Security Guard'),
        ('GENERAL_HELPER', 'General Labor & Loading'),
        ('GARDENING', 'Gardening & Maintenance'),
        ('DELIVERY', 'Delivery & Logistics Helper'),
    )

    STATUS_CHOICES = (
        ('OPEN', 'Open for Bidding / Applying'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    PAY_TYPE_CHOICES = (
        ('DAILY', 'Per Day (Daily Wage)'),
        ('FIXED', 'Fixed Lump-sum'),
        ('HOURLY', 'Per Hour'),
    )

    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200, help_text="e.g. Need 2 Painters for 2BHK Apartment")
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='CONSTRUCTION')
    description = models.TextField()
    required_skill = models.CharField(max_length=150, help_text="e.g. Wall putty, emulsion paint, exterior primer")
    
    city = models.CharField(max_length=100, default='Bengaluru')
    location = models.CharField(max_length=255, help_text="e.g. Indiranagar 12th Main, Near Metro Station")
    estimated_distance_km = models.DecimalField(max_digits=4, decimal_places=1, default=2.5, help_text="Estimated distance for worker view")
    radius_km = models.PositiveIntegerField(default=5, help_text="Priority radius in km set by user/contractor")
    priority_window_minutes = models.PositiveIntegerField(default=30, help_text="Match timing window: nearby workers informed first")
    
    pay_offered = models.DecimalField(max_digits=8, decimal_places=2, help_text="Wage offered (e.g. 850.00)")
    pay_type = models.CharField(max_length=20, choices=PAY_TYPE_CHOICES, default='DAILY')
    duration = models.CharField(max_length=100, default='1 Day (8:30 AM - 5:30 PM)')
    
    workers_required = models.PositiveIntegerField(default=1)
    workers_hired = models.PositiveIntegerField(default=0)
    
    contact_phone = models.CharField(max_length=15)
    contact_person = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    start_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_filled(self):
        return self.workers_hired >= self.workers_required

    @property
    def is_in_priority_window(self):
        from datetime import timedelta
        if not self.created_at:
            return False
        return timezone.now() < (self.created_at + timedelta(minutes=self.priority_window_minutes))

    def distance_from_worker(self, worker_user):
        from .utils import calculate_distance_between
        worker_loc = getattr(worker_user, 'locality', '') or getattr(worker_user, 'city', '')
        return calculate_distance_between(self.location, worker_loc)

    def is_worker_nearby(self, worker_user):
        return self.distance_from_worker(worker_user) <= self.radius_km

    def __str__(self):
        return f"{self.title} - ₹{self.pay_offered} ({self.location})"


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('APPLIED', 'Application Submitted'),
        ('ACCEPTED', 'Accepted & Hired'),
        ('REJECTED', 'Not Selected'),
        ('COMPLETED', 'Work Completed'),
        ('PAID', 'Payment Settled'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    worker_note = models.TextField(blank=True, help_text="Worker message or readiness note")
    contractor_feedback = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'worker')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.worker.get_full_name() or self.worker.username} -> {self.job.title} [{self.status}]"


class Review(models.Model):
    ROLE_CHOICES = (
        ('WORKER', 'Review of Worker by Contractor'),
        ('CONTRACTOR', 'Review of Contractor by Worker'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    target_role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # For Worker Review (Rated by Contractor)
    punctuality_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    work_quality_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    communication_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    reliability_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")

    # For Contractor Review (Rated by Worker)
    timely_payment_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    professional_behavior_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    job_accuracy_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    safety_conditions_score = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")

    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.reviewer} for {self.reviewee} ({self.overall_rating}★)"


class WalletTransaction(models.Model):
    TX_TYPE_CHOICES = (
        ('EARNING', 'Job Earnings Credited'),
        ('PENDING_PAYMENT', 'Pending Contractor Clearance'),
        ('WITHDRAWAL', 'Transferred to Bank / UPI'),
    )

    STATUS_CHOICES = (
        ('COMPLETED', 'Completed'),
        ('PENDING', 'Pending Clearance'),
        ('FAILED', 'Failed'),
    )

    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet_transactions')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, related_name='wallet_records')
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TX_TYPE_CHOICES, default='EARNING')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.worker.username}: ₹{self.amount} - {self.transaction_type} ({self.status})"
