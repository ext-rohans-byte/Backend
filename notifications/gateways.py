from django.core.mail import send_mail
from django.conf import settings


class EmailNotificationGateway:
    def send(self, *, user, subject, message):
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
