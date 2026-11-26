"""
Website models.

The site's content is still static (see pages.py and content.py). The one
thing that must be stored is what visitors send us: every enquiry is saved
here first, then emailed, so a message is never lost because mail failed or
is not configured yet. Enquiries are read and marked handled in the admin.
"""

from django.db import models

ENQUIRY_TYPES = [
    ("community", "Community / household"),
    ("government", "Government or NGO"),
    ("partner", "Partner"),
    ("finance", "Buyer or investor"),
    ("other", "Other"),
]

ENQUIRY_SUBJECTS = [
    ("general", "General enquiry"),
    ("partnership", "Partnership"),
    ("carbon", "Carbon credits and climate finance"),
    ("rooftop", "Rooftop solar owners"),
    ("community", "Bringing the Green ICS to my community"),
    ("press", "Media and press"),
    ("careers", "Careers"),
]


class Enquiry(models.Model):
    created_at = models.DateTimeField("received", auto_now_add=True, db_index=True)

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField("phone or WhatsApp", max_length=40, blank=True)
    enquiry_type = models.CharField("I am a", max_length=20, choices=ENQUIRY_TYPES, blank=True)
    subject = models.CharField(max_length=20, choices=ENQUIRY_SUBJECTS)
    message = models.TextField(max_length=2000)

    # Delivery: set when the notification email went out, or why it did not.
    emailed_at = models.DateTimeField(null=True, blank=True)
    email_error = models.TextField(blank=True)

    # Follow-up, for whoever answers enquiries.
    handled = models.BooleanField(default=False, db_index=True)
    notes = models.TextField("internal notes", blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "enquiries"

    def __str__(self) -> str:
        return f"{self.name} — {self.get_subject_display()}"
