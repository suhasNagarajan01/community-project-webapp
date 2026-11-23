from notifications.models import Notification

def user_theme_context(request):
    """
    Supplies active theme (green/emerald vs brown/beige), dark/light mode,
    and user unread notification counts to all templates.
    """
    theme = 'green'
    mode = 'light'
    unread_notifications_count = 0

    if request.user.is_authenticated:
        theme = getattr(request.user, 'theme_preference', 'green')
        mode = getattr(request.user, 'color_mode', 'light')
        try:
            unread_notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        except Exception:
            unread_notifications_count = 0
    else:
        # Check session for unauthenticated visitors
        theme = request.session.get('theme_preference', 'green')
        mode = request.session.get('color_mode', 'light')

    return {
        'current_theme': theme,
        'current_mode': mode,
        'unread_notifications_count': unread_notifications_count,
    }
