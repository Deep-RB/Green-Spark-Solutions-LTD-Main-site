from django.contrib import admin

from .models import Enquiry

admin.site.site_header = "Green Spark website"
admin.site.site_title = "Green Spark website admin"
admin.site.index_title = "Website administration"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "email", "subject", "enquiry_type", "emailed", "handled")
    list_filter = ("handled", "subject", "enquiry_type", "created_at")
    list_editable = ("handled",)
    search_fields = ("name", "email", "phone", "message")
    date_hierarchy = "created_at"
    readonly_fields = (
        "created_at", "name", "email", "phone", "enquiry_type", "subject", "message",
        "emailed_at", "email_error",
    )
    fieldsets = (
        (None, {"fields": ("created_at", "name", "email", "phone", "enquiry_type", "subject", "message")}),
        ("Follow-up", {"fields": ("handled", "notes")}),
        ("Email notification", {"fields": ("emailed_at", "email_error"), "classes": ("collapse",)}),
    )

    @admin.display(boolean=True, description="emailed")
    def emailed(self, obj):
        return obj.emailed_at is not None

    def has_add_permission(self, request):
        # Enquiries come from the website form only.
        return False
