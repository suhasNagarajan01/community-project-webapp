from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job_view, name='post_job'),
    path('<int:pk>/', views.job_detail_view, name='job_detail'),
    path('<int:pk>/apply/', views.apply_job_view, name='apply_job'),
    path('contractor/manage/', views.contractor_jobs_view, name='contractor_jobs'),
    path('contractor/manage/<int:pk>/', views.contractor_job_applicants_view, name='contractor_job_applicants'),
    path('applications/<int:app_id>/<str:action>/', views.update_application_status, name='update_application_status'),
    path('reviews/add/<int:job_id>/<int:reviewee_id>/', views.create_review_view, name='create_review'),
]
