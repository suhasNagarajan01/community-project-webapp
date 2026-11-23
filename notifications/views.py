from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list_view(request):
    """Feed of user notifications with mark-as-read."""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    # Mark all as read upon opening
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })


@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notif.is_read = True
    notif.save(update_fields=['is_read'])
    # Security check: prevent open redirects by verifying internal relative URL
    if notif.link and notif.link.startswith('/') and not notif.link.startswith('//'):
        return redirect(notif.link)
    return redirect('notification_list')
