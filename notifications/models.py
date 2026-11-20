from django.db import models
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=40,
        default='INFO',
        choices=[
            ('JOB_APPLIED', 'Job Application Received'),
            ('JOB_ACCEPTED', 'Application Accepted'),
            ('PAYMENT_CREDITED', 'Payment Credited'),
            ('REVIEW_RECEIVED', 'New Review'),
            ('CHAT_MESSAGE', 'New Message'),
            ('INFO', 'System Information'),
        ]
    )
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
