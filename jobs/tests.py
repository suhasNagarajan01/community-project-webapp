from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, WorkerProfile, ContractorProfile
from jobs.models import Job, JobApplication, Review, WalletTransaction
from decimal import Decimal

class DailyWagePlatformTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create Worker
        self.worker_user = User.objects.create_user(
            username='test_worker',
            password='password123',
            role='WORKER',
            first_name='Raju Worker',
            phone_number='9876543210',
            locality='Indiranagar'
        )
        self.worker_profile = WorkerProfile.objects.create(
            user=self.worker_user,
            skills='Electrician, Plumber',
            expected_daily_wage=Decimal('800.00'),
            rating=Decimal('4.80'),
            reliability_score=95,
            attendance_score=98,
            completed_jobs_count=10
        )

        # Create Contractor
        self.contractor_user = User.objects.create_user(
            username='test_contractor',
            password='password123',
            role='CONTRACTOR',
            first_name='Kiran Contractor',
            phone_number='9845012345',
            locality='Koramangala'
        )
        self.contractor_profile = ContractorProfile.objects.create(
            user=self.contractor_user,
            company_name='Kiran BuildTech',
            business_type='Construction Contractor'
        )

        # Create Job
        self.job = Job.objects.create(
            contractor=self.contractor_user,
            title='Test Masonry Work',
            category='CONSTRUCTION',
            description='Test job description',
            required_skill='Masonry',
            location='Koramangala',
            pay_offered=Decimal('900.00'),
            workers_required=2,
            contact_phone='9845012345'
        )

    def test_worker_ranking_calculation(self):
        score = self.worker_profile.recalculate_ranking()
        self.assertGreater(score, 70.0)

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RojgarSetu')
        self.assertContains(response, 'Worker Portal')

    def test_worker_application_flow(self):
        self.client.login(username='test_worker', password='password123')
        
        # Apply for job
        response = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'worker_note': 'Ready to start immediately'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        app = JobApplication.objects.filter(job=self.job, worker=self.worker_user).first()
        self.assertIsNotNone(app)
        self.assertEqual(app.status, 'APPLIED')

    def test_contractor_hiring_and_completion_flow(self):
        # Create application
        app = JobApplication.objects.create(
            job=self.job,
            worker=self.worker_user,
            status='APPLIED'
        )

        self.client.login(username='test_contractor', password='password123')

        # Contractor hires worker
        response = self.client.get(reverse('update_application_status', args=[app.id, 'accept']), follow=True)
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.status, 'ACCEPTED')

        # Contractor completes work and triggers payout
        response = self.client.get(reverse('update_application_status', args=[app.id, 'complete']), follow=True)
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.status, 'COMPLETED')

        # Verify wallet credit
        wallet_tx = WalletTransaction.objects.filter(worker=self.worker_user, job=self.job).first()
        self.assertIsNotNone(wallet_tx)
        self.assertEqual(wallet_tx.amount, Decimal('900.00'))

    def test_theme_toggle_api(self):
        response = self.client.post(reverse('toggle_theme'), {
            'theme': 'brown',
            'mode': 'dark'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['theme'], 'brown')
        self.assertEqual(data['mode'], 'dark')
