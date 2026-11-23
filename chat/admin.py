from django.contrib import admin
from .models import Conversation, ChatMessage

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'contractor', 'worker', 'job', 'updated_at')
    search_fields = ('contractor__username', 'worker__username')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
