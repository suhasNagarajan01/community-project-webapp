from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('WORKER', 'Daily Wage Worker'),
        ('CONTRACTOR', 'Contractor / Employer'),
        ('ADMIN', 'Administrator'),
    )
    THEME_CHOICES = (
        ('green', 'Emerald & Crisp White (Default)'),
        ('brown', 'Warm Earth & Soft Beige'),
    )
    COLOR_MODE_CHOICES = (
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='WORKER')
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, default='Bengaluru')
    locality = models.CharField(max_length=120, blank=True, help_text="e.g. Indiranagar, Koramangala, Whitefield")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    theme_preference = models.CharField(max_length=20, choices=THEME_CHOICES, default='green')
    color_mode = models.CharField(max_length=10, choices=COLOR_MODE_CHOICES, default='light')

    @property
    def is_worker(self):
        return self.role == 'WORKER'

    @property
    def is_contractor(self):
        return self.role == 'CONTRACTOR'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class WorkerProfile(models.Model):
    AVAILABILITY_CHOICES = (
        ('AVAILABLE', 'Available Today'),
        ('BUSY', 'Currently Working'),
        ('UNAVAILABLE', 'Unavailable'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    skills = models.CharField(max_length=255, help_text="Comma-separated: e.g. Electrician, Plumber, Housekeeping")
    languages_known = models.CharField(max_length=255, default="Kannada, Hindi, English")
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=2.0)
    expected_daily_wage = models.DecimalField(max_digits=8, decimal_places=2, default=750.00)
    bio = models.TextField(blank=True, default="Experienced and reliable worker available for daily assignments.")
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='AVAILABLE')
    
    # Reputation & ranking metrics
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.85)
    total_ratings_count = models.PositiveIntegerField(default=12)
    reliability_score = models.IntegerField(default=96, help_text="Score 0-100")
    attendance_score = models.IntegerField(default=98, help_text="Score 0-100")
    completed_jobs_count = models.PositiveIntegerField(default=24)
    ranking_score = models.FloatField(default=92.5)

    def skill_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def language_list(self):
        return [l.strip() for l in self.languages_known.split(',') if l.strip()]

    def recalculate_ranking(self):
        # Ranking formula factoring rating (40%), reliability (30%), attendance (20%), completed jobs (10%)
        rating_pct = (float(self.rating) / 5.0) * 100.0
        score = (rating_pct * 0.40) + (self.reliability_score * 0.30) + (self.attendance_score * 0.20) + (min(self.completed_jobs_count, 50) * 0.20)
        self.ranking_score = round(score, 2)
        self.save(update_fields=['ranking_score'])
        return self.ranking_score

    def __str__(self):
        return f"Worker: {self.user.get_full_name() or self.user.username} - {self.skills}"


class ContractorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contractor_profile')
    company_name = models.CharField(max_length=150, blank=True, help_text="Company or Contractor name")
    business_type = models.CharField(
        max_length=60,
        default='Individual / Household',
        choices=[
            ('Individual / Household', 'Individual / Household'),
            ('Construction Contractor', 'Construction Contractor'),
            ('Facility Management', 'Facility Management'),
            ('Interior & Renovation', 'Interior & Renovation'),
            ('Event & Catering', 'Event & Catering'),
            ('Small Enterprise', 'Small Enterprise'),
        ]
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.90)
    total_ratings_count = models.PositiveIntegerField(default=18)
    is_verified = models.BooleanField(default=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Contractor: {self.company_name or self.user.get_full_name() or self.user.username}"
