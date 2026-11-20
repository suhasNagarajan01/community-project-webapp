from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, WorkerProfile, ContractorProfile
from jobs.models import Job, JobApplication, Review, WalletTransaction
from chat.models import Conversation, ChatMessage
from notifications.models import Notification
from decimal import Decimal
import datetime

class Command(BaseCommand):
    help = 'Seeds realistic sample data for the Daily Wage Platform (Workers, Contractors, Jobs, Wallet, Chat, Reviews)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Clearing old data or populating seed data..."))

        # Create Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'System',
                'last_name': 'Administrator',
                'email': 'admin@rojgarsetu.in',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Admin account created (admin / admin123)"))

        # Seed Contractors
        contractors_data = [
            {
                'username': 'buildwell_infra',
                'first_name': 'Rajesh Sharma',
                'phone': '9845012345',
                'locality': 'Koramangala 4th Block',
                'company': 'BuildWell Infrastructure & Construction',
                'btype': 'Construction Contractor',
                'rating': Decimal('4.92'),
                'reviews_count': 26,
            },
            {
                'username': 'prestige_homes',
                'first_name': 'Suresh Reddy',
                'phone': '9880054321',
                'locality': 'Indiranagar 100ft Road',
                'company': 'Prestige Home Renovations',
                'btype': 'Interior & Renovation',
                'rating': Decimal('4.88'),
                'reviews_count': 19,
            },
            {
                'username': 'urban_facility',
                'first_name': 'Anita Deshmukh',
                'phone': '9741122334',
                'locality': 'HSR Layout Sector 2',
                'company': 'Urban Clean & Facility Services',
                'btype': 'Facility Management',
                'rating': Decimal('4.95'),
                'reviews_count': 34,
            },
            {
                'username': 'household_anand',
                'first_name': 'Anand Murthy',
                'phone': '9844098765',
                'locality': 'Jayanagar 4th T Block',
                'company': 'Anand Murthy (Private Residence)',
                'btype': 'Individual / Household',
                'rating': Decimal('5.00'),
                'reviews_count': 8,
            }
        ]

        contractor_objs = []
        for c in contractors_data:
            user, u_created = User.objects.get_or_create(
                username=c['username'],
                defaults={
                    'first_name': c['first_name'],
                    'role': 'CONTRACTOR',
                    'phone_number': c['phone'],
                    'city': 'Bengaluru',
                    'locality': c['locality'],
                }
            )
            if u_created:
                user.set_password('contractor123')
                user.save()

            cp, cp_created = ContractorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'company_name': c['company'],
                    'business_type': c['btype'],
                    'rating': c['rating'],
                    'total_ratings_count': c['reviews_count'],
                    'is_verified': True,
                    'address': f"{c['locality']}, Bengaluru, Karnataka",
                }
            )
            contractor_objs.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(contractor_objs)} Contractors"))

        # Seed Workers
        workers_data = [
            {
                'username': 'ramesh_kumar',
                'name': 'Ramesh Kumar',
                'phone': '9876543210',
                'locality': 'Indiranagar',
                'skills': 'Electrician, Inverter Wiring, DB Box Fitting, Appliance Repair',
                'languages': 'Kannada, Hindi, English',
                'exp': Decimal('5.5'),
                'wage': Decimal('850.00'),
                'rating': Decimal('4.94'),
                'reviews_count': 32,
                'reliability': 99,
                'attendance': 98,
                'completed': 48,
                'bio': 'Certified electrician with 5+ years handling residential and commercial wiring, MCB replacements, and switchboard fittings.',
            },
            {
                'username': 'manjunath_plumber',
                'name': 'Manjunath Gowda',
                'phone': '9845112233',
                'locality': 'Koramangala',
                'skills': 'Plumbing, CPVC Piping, Sanitary Fitting, Overhead Tank Cleaning',
                'languages': 'Kannada, Tamil, Telugu',
                'exp': Decimal('7.0'),
                'wage': Decimal('900.00'),
                'rating': Decimal('4.89'),
                'reviews_count': 28,
                'reliability': 97,
                'attendance': 99,
                'completed': 54,
                'bio': 'Fast and clean plumbing expert. Specialized in leak detection, pressure pumps, bathroom remodeling, and pipeline joints.',
            },
            {
                'username': 'sunil_painter',
                'name': 'Sunil Verma',
                'phone': '9731234567',
                'locality': 'Whitefield',
                'skills': 'Painting, Wall Putty, Texture Coating, Exterior Primer',
                'languages': 'Hindi, Kannada',
                'exp': Decimal('4.0'),
                'wage': Decimal('800.00'),
                'rating': Decimal('4.82'),
                'reviews_count': 21,
                'reliability': 95,
                'attendance': 96,
                'completed': 38,
                'bio': 'Skilled painter for interior and exterior walls. Expert at roller finish, waterproofing putty, and spray enamel.',
            },
            {
                'username': 'lakshmi_housekeeping',
                'name': 'Lakshmi Devi',
                'phone': '9886765432',
                'locality': 'HSR Layout',
                'skills': 'Housekeeping, Deep Cleaning, Floor Scrubbing, Event Helpers',
                'languages': 'Kannada, Telugu, Hindi',
                'exp': Decimal('3.5'),
                'wage': Decimal('700.00'),
                'rating': Decimal('4.96'),
                'reviews_count': 42,
                'reliability': 100,
                'attendance': 99,
                'completed': 62,
                'bio': 'Punctual and meticulous cleaning staff for residential deep cleans, post-renovation cleanups, and catering help.',
            },
            {
                'username': 'arun_mason',
                'name': 'Arun Swamy',
                'phone': '9945009988',
                'locality': 'Jayanagar',
                'skills': 'Construction, Masonry, Tile Laying, Brickwork, Plastering',
                'languages': 'Tamil, Kannada',
                'exp': Decimal('6.0'),
                'wage': Decimal('950.00'),
                'rating': Decimal('4.85'),
                'reviews_count': 19,
                'reliability': 96,
                'attendance': 97,
                'completed': 41,
                'bio': 'Experienced mason specialized in precision tile laying, concrete mixing, boundary walls, and structural plastering.',
            },
            {
                'username': 'deepak_helper',
                'name': 'Deepak Yadav',
                'phone': '9740556677',
                'locality': 'BTM Layout',
                'skills': 'General Helper, Material Loading, Debris Clearing, Shifting',
                'languages': 'Hindi, Bhojpuri, Kannada',
                'exp': Decimal('2.0'),
                'wage': Decimal('650.00'),
                'rating': Decimal('4.78'),
                'reviews_count': 15,
                'reliability': 94,
                'attendance': 95,
                'completed': 29,
                'bio': 'Energetic general labor helper ready for heavy lifting, warehouse unloading, construction shifting, and garden cleaning.',
            },
            {
                'username': 'praveen_carpenter',
                'name': 'Praveen Acharya',
                'phone': '9900887766',
                'locality': 'Marathahalli',
                'skills': 'Carpentry, Furniture Assembly, Door Lock Fitting, Wood Polish',
                'languages': 'Kannada, Hindi, English',
                'exp': Decimal('8.0'),
                'wage': Decimal('1000.00'),
                'rating': Decimal('4.97'),
                'reviews_count': 35,
                'reliability': 98,
                'attendance': 100,
                'completed': 58,
                'bio': 'Master carpenter for modular kitchen fixes, custom cabinets, laminate repairs, and emergency door hardware replacement.',
            },
            {
                'username': 'somesh_security',
                'name': 'Someshwar Rao',
                'phone': '9845998877',
                'locality': 'Electronic City',
                'skills': 'Security Guard, Night Watchman, Gate Access Control, Event Security',
                'languages': 'Kannada, Telugu, Hindi',
                'exp': Decimal('5.0'),
                'wage': Decimal('750.00'),
                'rating': Decimal('4.88'),
                'reviews_count': 23,
                'reliability': 99,
                'attendance': 98,
                'completed': 36,
                'bio': 'Ex-serviceman disciplined security guard for apartment gates, construction site watch, and corporate events.',
            }
        ]

        worker_objs = []
        for w in workers_data:
            user, u_created = User.objects.get_or_create(
                username=w['username'],
                defaults={
                    'first_name': w['name'],
                    'role': 'WORKER',
                    'phone_number': w['phone'],
                    'city': 'Bengaluru',
                    'locality': w['locality'],
                }
            )
            if u_created:
                user.set_password('worker123')
                user.save()

            wp, wp_created = WorkerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'skills': w['skills'],
                    'languages_known': w['languages'],
                    'experience_years': w['exp'],
                    'expected_daily_wage': w['wage'],
                    'rating': w['rating'],
                    'total_ratings_count': w['reviews_count'],
                    'reliability_score': w['reliability'],
                    'attendance_score': w['attendance'],
                    'completed_jobs_count': w['completed'],
                    'bio': w['bio'],
                }
            )
            wp.recalculate_ranking()
            worker_objs.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(worker_objs)} Workers"))

        # Seed Jobs
        jobs_data = [
            {
                'contractor': contractor_objs[0], # BuildWell Infra
                'title': 'Need 3 Skilled Masons for Commercial Building Plastering',
                'category': 'CONSTRUCTION',
                'skill': 'Masonry, Plastering, Brickwork',
                'desc': 'Urgent requirement for 3 experienced masons for interior brickwork and cement plastering on the 2nd floor of our commercial project. Lunch provided on site. Daily payout after 5:30 PM inspection.',
                'location': 'Koramangala 80ft Road, Near Sony World',
                'dist': Decimal('1.4'),
                'pay': Decimal('950.00'),
                'duration': '3 Days (8:30 AM - 5:30 PM)',
                'req': 3,
                'hired': 1,
                'phone': '9845012345',
                'person': 'Rajesh Sharma (Supervisor)',
            },
            {
                'contractor': contractor_objs[1], # Prestige Renovations
                'title': 'Urgent 2 Electricians for 3BHK Concealed Conduit Wiring',
                'category': 'ELECTRICAL',
                'skill': 'Conduit wiring, Distribution Box, Inverter hookup',
                'desc': 'Complete rewiring of 3BHK flat in Indiranagar. Need 2 qualified electricians with tools. Wall chasing already completed. High daily wage with performance bonus.',
                'location': 'Indiranagar 12th Main, Near Metro Station',
                'dist': Decimal('2.1'),
                'pay': Decimal('900.00'),
                'duration': '2 Days (9:00 AM - 6:00 PM)',
                'req': 2,
                'hired': 1,
                'phone': '9880054321',
                'person': 'Suresh Reddy (Site Lead)',
            },
            {
                'contractor': contractor_objs[1], # Prestige Renovations
                'title': 'Need 4 Painters for Apartment Interior Putty & Emulsion Coating',
                'category': 'PAINTING',
                'skill': 'Wall Putty sanding, Asian Paints Royale application, Roller finish',
                'desc': 'Fresh repainting project for residential duplex. Scaffolding and ladders on site. Looking for 4 painters with neat cutting and masking tape experience.',
                'location': 'Defence Colony, Indiranagar',
                'dist': Decimal('2.8'),
                'pay': Decimal('850.00'),
                'duration': '4 Days (9:00 AM - 5:30 PM)',
                'req': 4,
                'hired': 2,
                'phone': '9880054321',
                'person': 'Mahesh (Foreman)',
            },
            {
                'contractor': contractor_objs[2], # Urban Clean
                'title': '3 Deep Cleaning Staff for Post-Construction Villa Cleanup',
                'category': 'HOUSEKEEPING',
                'skill': 'Floor scrubber operation, Window glass cleaning, Chemical grout removal',
                'desc': 'Immediate requirement for 3 housekeeping workers for 4500 sq ft luxury villa handover. High-pressure wash and tile scrubbing machines provided.',
                'location': 'HSR Layout Sector 1, 27th Main',
                'dist': Decimal('3.5'),
                'pay': Decimal('750.00'),
                'duration': '1 Day (9:30 AM - 6:00 PM)',
                'req': 3,
                'hired': 0,
                'phone': '9741122334',
                'person': 'Anita Deshmukh',
            },
            {
                'contractor': contractor_objs[3], # Anand Murthy (Private)
                'title': 'Plumber Needed for Leaking Overhead Tank & Bathroom Valves',
                'category': 'PLUMBING',
                'skill': 'Overhead Sintex pipe connection, Ball valve replacement',
                'desc': 'Main PVC line from overhead tank has developed a split. Need one experienced plumber to replace 1.5 inch pipe and 2 ball valves in our residence.',
                'location': 'Jayanagar 4th Block, 9th Cross',
                'dist': Decimal('1.8'),
                'pay': Decimal('850.00'),
                'duration': 'Half Day / 1 Day (10:00 AM - 2:00 PM)',
                'req': 1,
                'hired': 0,
                'phone': '9844098765',
                'person': 'Anand Murthy',
            },
            {
                'contractor': contractor_objs[0], # BuildWell Infra
                'title': 'Need 4 General Labor Helpers for Unloading Cement & Sand Sacks',
                'category': 'GENERAL_HELPER',
                'skill': 'Heavy material shifting, Sand sieving, Site clearing',
                'desc': 'Truck shipment arriving at 9 AM with 200 bags of Ultratech cement. Need 4 physically fit helpers to unload and stack into the storage shed.',
                'location': 'Ejipura Main Road, Near Ring Road',
                'dist': Decimal('2.4'),
                'pay': Decimal('700.00'),
                'duration': '1 Day (9:00 AM - 4:30 PM)',
                'req': 4,
                'hired': 1,
                'phone': '9845012345',
                'person': 'Rajesh Sharma',
            },
            {
                'contractor': contractor_objs[2], # Urban Clean
                'title': '2 Night Security Guards for Construction Compound Watch',
                'category': 'SECURITY',
                'skill': 'Site perimeter patrol, Entry register logging, Torch watch',
                'desc': 'Requirement for 2 vigilant night watchmen to secure raw materials and equipment stored in open construction yard. Safe cabin with power and hot water.',
                'location': 'Kudlu Gate, Near Hosur Road',
                'dist': Decimal('4.2'),
                'pay': Decimal('800.00'),
                'duration': 'Night Shift (8:00 PM - 8:00 AM)',
                'req': 2,
                'hired': 0,
                'phone': '9741122334',
                'person': 'Raju Security Lead',
            },
            {
                'contractor': contractor_objs[1], # Prestige Renovations
                'title': 'Carpenter for Wardrobe Shutter Alignment & Hinges Repair',
                'category': 'CARPENTRY',
                'skill': 'Hydraulic soft-close hinges, sliding wardrobe channels',
                'desc': 'Need an experienced carpenter to refit 6 wardrobe shutters and adjust German hydraulic soft-close hinges in an apartment.',
                'location': 'Old Airport Road, Kodihalli',
                'dist': Decimal('3.1'),
                'pay': Decimal('1000.00'),
                'duration': '1 Day (10:00 AM - 6:00 PM)',
                'req': 1,
                'hired': 0,
                'phone': '9880054321',
                'person': 'Suresh Reddy',
            }
        ]

        created_jobs = []
        for jd in jobs_data:
            job, j_created = Job.objects.get_or_create(
                title=jd['title'],
                contractor=jd['contractor'],
                defaults={
                    'category': jd['category'],
                    'required_skill': jd['skill'],
                    'description': jd['desc'],
                    'city': 'Bengaluru',
                    'location': jd['location'],
                    'estimated_distance_km': jd['dist'],
                    'pay_offered': jd['pay'],
                    'pay_type': 'DAILY',
                    'duration': jd['duration'],
                    'workers_required': jd['req'],
                    'workers_hired': jd['hired'],
                    'contact_phone': jd['phone'],
                    'contact_person': jd['person'],
                    'status': 'OPEN',
                    'start_date': timezone.now().date() + datetime.timedelta(days=1),
                }
            )
            created_jobs.append(job)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_jobs)} Jobs"))

        # Seed sample Applications
        # Ramesh Kumar applied to Job 1 (Electrical)
        JobApplication.objects.get_or_create(
            job=created_jobs[1],
            worker=worker_objs[0],
            defaults={
                'status': 'ACCEPTED',
                'worker_note': 'I have my own drill machine and multi-meter. Can start tomorrow 9 AM.',
            }
        )

        # Sunil Verma applied to Job 2 (Painting)
        JobApplication.objects.get_or_create(
            job=created_jobs[2],
            worker=worker_objs[2],
            defaults={
                'status': 'APPLIED',
                'worker_note': 'Expert in Asian paints putty and roller work. Available immediately.',
            }
        )

        # Seed sample Wallet Transactions for Ramesh Kumar
        WalletTransaction.objects.get_or_create(
            worker=worker_objs[0],
            description="Daily wage: 2BHK Main MCB Box Wiring & Inverter Setup",
            amount=Decimal('850.00'),
            defaults={
                'transaction_type': 'EARNING',
                'status': 'COMPLETED',
                'created_at': timezone.now() - datetime.timedelta(days=2),
            }
        )
        WalletTransaction.objects.get_or_create(
            worker=worker_objs[0],
            description="Daily wage: Commercial Shop Lighting Circuit Installation",
            amount=Decimal('900.00'),
            defaults={
                'transaction_type': 'EARNING',
                'status': 'COMPLETED',
                'created_at': timezone.now() - datetime.timedelta(days=1),
            }
        )
        WalletTransaction.objects.get_or_create(
            worker=worker_objs[0],
            description="Direct UPI payout to 9876543210@upi",
            amount=Decimal('1000.00'),
            defaults={
                'transaction_type': 'WITHDRAWAL',
                'status': 'COMPLETED',
                'created_at': timezone.now() - datetime.timedelta(hours=12),
            }
        )

        # Seed sample Review
        Review.objects.get_or_create(
            job=created_jobs[1],
            reviewer=contractor_objs[1],
            reviewee=worker_objs[0],
            defaults={
                'target_role': 'WORKER',
                'punctuality_score': 5,
                'work_quality_score': 5,
                'communication_score': 5,
                'reliability_score': 5,
                'overall_rating': Decimal('5.00'),
                'comment': 'Ramesh did an outstanding job with concealed wiring. Very punctual, arrived at 8:45 AM, and left the site spotless!',
            }
        )

        # Seed sample Conversation and Chat message
        conv, _ = Conversation.objects.get_or_create(
            contractor=contractor_objs[1],
            worker=worker_objs[0],
            job=created_jobs[1]
        )
        ChatMessage.objects.get_or_create(
            conversation=conv,
            sender=contractor_objs[1],
            message="Hello Ramesh, can you please bring 2.5 sq mm copper wire cutter tomorrow?",
            defaults={'is_read': True}
        )
        ChatMessage.objects.get_or_create(
            conversation=conv,
            sender=worker_objs[0],
            message="Yes Suresh sir, I have the heavy-duty wire cutter and crimping tool. I will reach at 8:45 AM.",
            defaults={'is_read': False}
        )

        # Seed Notification for Ramesh
        Notification.objects.get_or_create(
            recipient=worker_objs[0],
            title="Congratulations! You are Hired",
            defaults={
                'message': "Prestige Home Renovations accepted your application for 'Urgent 2 Electricians for 3BHK Conduit Wiring'.",
                'notification_type': 'JOB_ACCEPTED',
                'link': f"/jobs/{created_jobs[1].id}/",
                'is_read': False
            }
        )

        self.stdout.write(self.style.SUCCESS("All sample data seeded successfully!"))
