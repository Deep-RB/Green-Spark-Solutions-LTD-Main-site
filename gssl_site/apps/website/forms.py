"""
The contact form, validated on the server.

The rules match static/js/components/forms.js, so a visitor whose browser
already passed the client-side checks is never rejected here; the server
checks are the ones that count.
"""

import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Enquiry

PHONE = re.compile(r"^\+?[\d\s\-()]{7,20}$")


class EnquiryForm(forms.ModelForm):
    # Honeypot: hidden from people, filled in by bots. Never stored.
    website = forms.CharField(required=False)

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "enquiry_type", "subject", "message"]
        error_messages = {
            "name": {"required": "This field is required."},
            "email": {
                "required": "This field is required.",
                "invalid": "Enter a valid email address, for example name@example.com.",
            },
            "subject": {"required": "This field is required."},
            "message": {"required": "This field is required."},
        }

    def clean_name(self):
        # Names go into the email subject line; keep them to one line.
        return " ".join(self.cleaned_data["name"].split())

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone and not PHONE.match(phone):
            raise ValidationError("Enter a valid phone number, including the country code.")
        return phone

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise ValidationError("Please write at least 10 characters.")
        return message

    def is_bot(self) -> bool:
        return bool(self.data.get("website", "").strip())
