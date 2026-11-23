from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Conversation, ChatMessage
from accounts.models import User
from jobs.models import Job
from notifications.models import Notification

@login_required
def chat_list_view(request):
    """Lists all active chat conversations for the logged in user."""
    user = request.user
    conversations = list(Conversation.objects.filter(
        Q(contractor=user) | Q(worker=user)
    ).select_related('contractor', 'worker', 'job').order_by('-updated_at'))

    for conv in conversations:
        conv.other_person = conv.get_other_user(user)

    return render(request, 'chat/chat_list.html', {
        'conversations': conversations
    })


@login_required
def chat_detail_view(request, conversation_id):
    """Chat room between Contractor and Worker with HTMX live message exchange."""
    user = request.user
    conversation = get_object_or_404(
        Conversation.objects.select_related('contractor', 'worker', 'job'),
        id=conversation_id
    )

    if user != conversation.contractor and user != conversation.worker:
        messages.error(request, "Access denied to this conversation.")
        return redirect('chat_list')

    # Mark received unread messages as read
    conversation.messages.filter(~Q(sender=user), is_read=False).update(is_read=True)

    other_user = conversation.worker if user == conversation.contractor else conversation.contractor

    if request.method == 'POST':
        text = request.POST.get('message', '').strip()
        if text:
            new_msg = ChatMessage.objects.create(
                conversation=conversation,
                sender=user,
                message=text
            )
            conversation.save() # triggers updated_at auto_now

            # Notification to recipient
            Notification.objects.create(
                recipient=other_user,
                title=f"Message from {user.get_full_name() or user.username}",
                message=text[:80],
                notification_type='CHAT_MESSAGE',
                link=f"/chat/{conversation.id}/"
            )

            if request.headers.get('HX-Request'):
                return render(request, 'chat/partials/single_message.html', {'message': new_msg, 'user': user})

        return redirect('chat_detail', conversation_id=conversation.id)

    chat_messages = conversation.messages.select_related('sender').all()

    if request.headers.get('HX-Request') and request.GET.get('poll') == 'true':
        return render(request, 'chat/partials/message_stream.html', {
            'messages': chat_messages,
            'user': user
        })

    return render(request, 'chat/chat_detail.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': chat_messages,
    })


@login_required
def start_chat_view(request, other_user_id, job_id=None):
    """Initiates or resumes a chat between a contractor and a worker."""
    user = request.user
    other_user = get_object_or_404(User, pk=other_user_id)
    job = get_object_or_404(Job, pk=job_id) if job_id else None

    if user.is_contractor:
        contractor = user
        worker = other_user
    else:
        worker = user
        contractor = other_user

    conversation, _ = Conversation.objects.get_or_create(
        contractor=contractor,
        worker=worker,
        job=job
    )
    return redirect('chat_detail', conversation_id=conversation.id)
