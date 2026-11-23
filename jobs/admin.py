from django.contrib import admin
from .models import Job, JobApplication, Review, WalletTransaction

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'contractor', 'category', 'pay_offered', 'location', 'workers_required', 'workers_hired', 'status', 'created_at')
    list_filter = ('category', 'status', 'pay_type', 'city')
    search_fields = ('title', 'description', 'location', 'required_skill', 'contractor__username')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'worker', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'worker__username')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('job', 'reviewer', 'reviewee', 'target_role', 'overall_rating', 'created_at')
    list_filter = ('target_role', 'overall_rating')
    search_fields = ('reviewer__username', 'reviewee__username', 'comment')

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('worker', 'amount', 'transaction_type', 'status', 'created_at')
    list_filter = ('transaction_type', 'status')
    search_fields = ('worker__username', 'description')
