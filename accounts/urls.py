from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='user_profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('settings/', views.settings_view, name='settings'),
    path('toggle-theme/', views.toggle_theme_api, name='toggle_theme'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
