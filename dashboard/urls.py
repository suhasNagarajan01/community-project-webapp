from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_router, name='dashboard_router'),
    path('worker/', views.worker_dashboard, name='worker_dashboard'),
    path('worker/wallet/', views.worker_wallet_view, name='worker_wallet'),
    path('worker/applications/', views.worker_applications_view, name='worker_applications'),
    path('contractor/', views.contractor_dashboard, name='contractor_dashboard'),
]
