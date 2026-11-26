"""Email notifications for enquiries."""

import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from .models import Enquiry

log = logging.getLogger(__name__)


def notify_enquiry(enquiry: Enquiry) -> bool:
    """
    Email a saved enquiry to ENQUIRY_RECIPIENTS. Never raises: the enquiry is
    already stored, so a mail failure is recorded on it and logged, and the
    visitor still sees that their message arrived.
    """
    if not settings.ENQUIRY_EMAIL_ENABLED:
        enquiry.email_error = "Email not configured (DJANGO_EMAIL_HOST is unset)."
        enquiry.save(update_fields=["email_error"])
        return False

    lines = [
        f"Name:     {enquiry.name}",
        f"Email:    {enquiry.email}",
        f"Phone:    {enquiry.phone or '-'}",
        f"I am a:   {enquiry.get_enquiry_type_display() or '-'}",
        f"Subject:  {enquiry.get_subject_display()}",
        f"Received: {timezone.localtime(enquiry.created_at):%d %b %Y, %H:%M %Z}",
        "",
        enquiry.message,
        "",
        "-- ",
        f"Sent from the contact form at {settings.SITE_URL}. Reply to this email to answer.",
    ]
    message = EmailMessage(
        subject=f"Website enquiry: {enquiry.get_subject_display()} — {enquiry.name}",
        body="\n".join(lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.ENQUIRY_RECIPIENTS,
        reply_to=[enquiry.email],
    )
    try:
        message.send(fail_silently=False)
    except Exception as exc:  # noqa: BLE001 - any mail failure is recorded, not raised
        log.exception("Enquiry %s saved but not emailed", enquiry.pk)
        enquiry.email_error = f"{type(exc).__name__}: {exc}"[:1000]
        enquiry.save(update_fields=["email_error"])
        return False

    enquiry.emailed_at = timezone.now()
    enquiry.email_error = ""
    enquiry.save(update_fields=["emailed_at", "email_error"])
    return True
