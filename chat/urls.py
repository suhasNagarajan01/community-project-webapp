from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list_view, name='chat_list'),
    path('<int:conversation_id>/', views.chat_detail_view, name='chat_detail'),
    path('start/<int:other_user_id>/', views.start_chat_view, name='start_chat'),
    path('start/<int:other_user_id>/<int:job_id>/', views.start_chat_view, name='start_chat_with_job'),
]
