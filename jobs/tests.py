from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, WorkerProfile, ContractorProfile
from jobs.models import Job, JobApplication, Review, WalletTransaction
from notifications.models import Notification
from decimal import Decimal

class DailyWagePlatformTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create Worker
        self.worker_user = User.objects.create_user(
            username='ramesh_kumar',
            password='worker123',
            role='WORKER',
            first_name='Ramesh Kumar',
            phone_number='9876543210',
            locality='Indiranagar'
        )
        self.worker_profile = WorkerProfile.objects.create(
            user=self.worker_user,
            skills='Electrician, Plumber',
            expected_daily_wage=Decimal('850.00'),
            rating=Decimal('4.94'),
            reliability_score=99,
            attendance_score=98,
            completed_jobs_count=10
        )

        # Create Contractor
        self.contractor_user = User.objects.create_user(
            username='buildwell_infra',
            password='contractor123',
            role='CONTRACTOR',
            first_name='Rajesh Sharma',
            phone_number='9845012345',
            locality='Koramangala'
        )
        self.contractor_profile = ContractorProfile.objects.create(
            user=self.contractor_user,
            company_name='BuildWell Infrastructure',
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
            workers_required=1,
            contact_phone='9845012345'
        )

    def test_worker_ranking_calculation(self):
        score = self.worker_profile.recalculate_ranking()
        self.assertGreater(score, 70.0)

    def test_home_page_loads_and_has_testimonials_marquee(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RojgarSetu')
        self.assertContains(response, 'Worker Portal')
        self.assertContains(response, 'testimonials-marquee-wrapper')
        self.assertContains(response, 'Trusted by Workers & Contractors')
        # Check that old sample postings block is removed
        self.assertNotContains(response, 'Recently Posted Daily Jobs')

    def test_login_page_has_presets_and_testimonials(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ramesh_kumar')
        self.assertContains(response, 'buildwell_infra')
        self.assertContains(response, 'testimonials-marquee-wrapper')

    def test_preset_worker_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'ramesh_kumar',
            'password': 'worker123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].role, 'WORKER')

    def test_preset_contractor_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'buildwell_infra',
            'password': 'contractor123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].role, 'CONTRACTOR')

    def test_worker_application_flow(self):
        self.client.login(username='ramesh_kumar', password='worker123')
        
        # Apply for job
        response = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'worker_note': 'Ready to start immediately'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        app = JobApplication.objects.filter(job=self.job, worker=self.worker_user).first()
        self.assertIsNotNone(app)
        self.assertEqual(app.status, 'APPLIED')

    def test_contractor_hiring_and_completion_idempotency(self):
        """Vulnerability test: verifies multiple 'complete' actions do NOT double-credit wallet."""
        app = JobApplication.objects.create(
            job=self.job,
            worker=self.worker_user,
            status='APPLIED'
        )

        self.client.login(username='buildwell_infra', password='contractor123')

        # Contractor hires worker
        response = self.client.get(reverse('update_application_status', args=[app.id, 'accept']), follow=True)
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.status, 'ACCEPTED')

        # Contractor completes work first time -> credits wallet
        response = self.client.get(reverse('update_application_status', args=[app.id, 'complete']), follow=True)
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.status, 'COMPLETED')

        initial_tx_count = WalletTransaction.objects.filter(worker=self.worker_user, job=self.job).count()
        self.assertEqual(initial_tx_count, 1)

        # Attempt to call complete a second time (replaying request)
        response2 = self.client.get(reverse('update_application_status', args=[app.id, 'complete']), follow=True)
        self.assertEqual(response2.status_code, 200)
        new_tx_count = WalletTransaction.objects.filter(worker=self.worker_user, job=self.job).count()
        # MUST still be 1 (no double spend / double credit)
        self.assertEqual(new_tx_count, 1)

    def test_wallet_withdrawal_validation(self):
        """Vulnerability test: ensures withdrawal cannot be negative, zero, or exceed balance."""
        self.client.login(username='ramesh_kumar', password='worker123')

        # Credit 500 to wallet
        WalletTransaction.objects.create(
            worker=self.worker_user,
            amount=Decimal('500.00'),
            transaction_type='EARNING',
            status='COMPLETED',
            description="Completed electrical repair"
        )

        # Try to withdraw negative amount
        self.client.post(reverse('worker_wallet'), {'withdraw_amount': '-50'})
        self.assertEqual(WalletTransaction.objects.filter(transaction_type='WITHDRAWAL').count(), 0)

        # Try to withdraw more than available balance (e.g. 1000 when only 500 available)
        self.client.post(reverse('worker_wallet'), {'withdraw_amount': '1000'})
        self.assertEqual(WalletTransaction.objects.filter(transaction_type='WITHDRAWAL').count(), 0)

        # Valid withdrawal of 200
        self.client.post(reverse('worker_wallet'), {'withdraw_amount': '200'})
        self.assertEqual(WalletTransaction.objects.filter(transaction_type='WITHDRAWAL').count(), 1)

    def test_open_redirect_protection(self):
        """Vulnerability test: notification link must reject external evil.com redirects."""
        self.client.login(username='ramesh_kumar', password='worker123')
        
        # Evil notification with external domain
        notif = Notification.objects.create(
            recipient=self.worker_user,
            title="Malicious link",
            message="Check this",
            link="https://evil-attacker.com/steal-creds"
        )
        response = self.client.get(reverse('mark_notification_read', args=[notif.id]), follow=False)
        # Should redirect to safe internal notification_list, NOT to evil-attacker.com
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('notification_list'))

    def test_theme_toggle_api(self):
        response = self.client.post(reverse('toggle_theme'), {
            'theme': 'brown',
            'mode': 'dark'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['theme'], 'brown')
        self.assertEqual(data['mode'], 'dark')

    def test_location_analysis_api(self):
        """Verifies location analysis API computes nearby workers and match timings."""
        response = self.client.get(reverse('analyze_location_api'), {
            'location': 'Indiranagar 100ft Road',
            'radius_km': '5'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('nearby_count', data)
        self.assertIn('match_timing_minutes', data)
        self.assertEqual(data['radius_km'], 5.0)

    def test_job_posting_with_radius_and_priority_alert(self):
        """Contractor posts job with 5km radius; nearby workers receive priority alert."""
        self.client.login(username='buildwell_infra', password='contractor123')
        response = self.client.post(reverse('post_job'), {
            'title': 'Urgent Electrical Wiring',
            'category': 'ELECTRICAL',
            'description': 'Need certified electrician for office renovation.',
            'required_skill': 'Electrician',
            'city': 'Bengaluru',
            'location': 'Indiranagar',
            'radius_km': '5',
            'priority_window_minutes': '30',
            'pay_offered': '950.00',
            'pay_type': 'DAILY',
            'duration': '1 Day',
            'workers_required': '1',
            'contact_phone': '9845012345',
            'start_date': '2026-12-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Check job was created with radius and window
        new_job = Job.objects.get(title='Urgent Electrical Wiring')
        self.assertEqual(new_job.radius_km, 5)
        self.assertEqual(new_job.priority_window_minutes, 30)

        # Worker in Indiranagar should have received priority alert
        priority_notifs = Notification.objects.filter(
            recipient=self.worker_user,
            title__icontains="Priority Job Alert"
        )
        self.assertGreaterEqual(priority_notifs.count(), 1)

    def test_all_portal_views_and_routes(self):
        """Comprehensive verification: checks that all platform routes render with 200 OK."""
        # Public routes
        for url_name in ['home', 'about', 'contact', 'login', 'register']:
            res = self.client.get(reverse(url_name))
            self.assertEqual(res.status_code, 200, f"Failed on public view: {url_name}")

        # Worker authenticated routes
        self.client.login(username='ramesh_kumar', password='worker123')
        worker_urls = [
            'worker_dashboard', 'worker_wallet', 'worker_applications',
            'profile', 'profile_edit', 'settings', 'chat_list', 'notification_list'
        ]
        for url_name in worker_urls:
            res = self.client.get(reverse(url_name))
            self.assertEqual(res.status_code, 200, f"Failed on worker view: {url_name}")

        # Job detail view
        res = self.client.get(reverse('job_detail', args=[self.job.id]))
        self.assertEqual(res.status_code, 200)

        # Contractor authenticated routes
        self.client.login(username='buildwell_infra', password='contractor123')
        contractor_urls = ['contractor_dashboard', 'post_job', 'contractor_jobs']
        for url_name in contractor_urls:
            res = self.client.get(reverse(url_name))
            self.assertEqual(res.status_code, 200, f"Failed on contractor view: {url_name}")

        res = self.client.get(reverse('contractor_job_applicants', args=[self.job.id]))
        self.assertEqual(res.status_code, 200)

        # Review page
        res = self.client.get(reverse('create_review', args=[self.job.id, self.worker_user.id]))
        self.assertEqual(res.status_code, 200)
