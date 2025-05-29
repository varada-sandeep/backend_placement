from django.db import models
from django.contrib.auth.models import User


class CompanyDrive(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    RESULTS_STATUS_CHOICES = [
        ("NOT_STARTED", "Not Started"),
        ("IN_PROCESS", "In Process"),
        ("PENDING", "Pending"),
        ("DECLARED", "Declared"),
    ]

    company_name = models.CharField(max_length=100)
    point_of_contact = models.CharField(max_length=100)
    year_of_passing = models.IntegerField()
    job_received_date = models.DateField()
    job_posted_date = models.DateField()
    job_posted_by = models.CharField(max_length=100)
    student_data_shared_date = models.DateField(null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    interview_posted_date = models.DateField(null=True, blank=True)
    results_declaration_status = models.CharField(
        max_length=20, choices=RESULTS_STATUS_CHOICES, default="NOT_STARTED"
    )
    results_declaration_date = models.DateField(null=True, blank=True)
    no_of_selects = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    # Additional metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_drives",blank=True
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="updated_drives",
    blank=True
    )

    def __str__(self):
        return (
            f"{self.company_name} - {self.interview_date or 'No interview scheduled'}"
        )

    def save(self, *args, **kwargs):
        # Automatically determine the status based on the current state
        if (
            self.results_declaration_status == "DECLARED"
            and self.no_of_selects is not None
        ):
            self.status = "COMPLETED"
        elif self.interview_date and self.student_data_shared_date:
            self.status = "IN_PROGRESS"
        else:
            self.status = "PENDING"

        super().save(*args, **kwargs)
