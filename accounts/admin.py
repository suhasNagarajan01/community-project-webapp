from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WorkerProfile, ContractorProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'city', 'theme_preference', 'is_staff')
    list_filter = ('role', 'city', 'theme_preference', 'color_mode', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Fields', {
            'fields': ('role', 'phone_number', 'city', 'locality', 'profile_picture', 'theme_preference', 'color_mode')
        }),
    )

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'expected_daily_wage', 'rating', 'reliability_score', 'attendance_score', 'completed_jobs_count', 'availability_status')
    list_filter = ('availability_status', 'expected_daily_wage')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'skills')

@admin.register(ContractorProfile)
class ContractorProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'business_type', 'rating', 'is_verified')
    list_filter = ('business_type', 'is_verified')
    search_fields = ('company_name', 'user__username', 'user__first_name', 'user__last_name')
