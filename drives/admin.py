from django.contrib import admin
from .models import CompanyDrive


class CompanyDriveAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "point_of_contact",
        "year_of_passing",
        "interview_date",
        "results_declaration_status",
        "no_of_selects",
        "status",
    )
    list_filter = ("status", "results_declaration_status", "year_of_passing")
    search_fields = ("company_name", "point_of_contact", "job_posted_by")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            "Company Information",
            {"fields": ("company_name", "point_of_contact", "year_of_passing")},
        ),
        (
            "Job Details",
            {"fields": ("job_received_date", "job_posted_date", "job_posted_by")},
        ),
        (
            "Interview Process",
            {
                "fields": (
                    "student_data_shared_date",
                    "interview_date",
                    "interview_posted_date",
                )
            },
        ),
        (
            "Results",
            {
                "fields": (
                    "results_declaration_status",
                    "results_declaration_date",
                    "no_of_selects",
                )
            },
        ),
        ("Status", {"fields": ("status",)}),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# Register the model with its admin
admin.site.register(CompanyDrive, CompanyDriveAdmin)
