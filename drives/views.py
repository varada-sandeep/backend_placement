# ===== drives/views.py - Updated with better error handling =====

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import CompanyDrive
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def is_staff(user):
    """Check if the user is authenticated and associated with a PlacementStaff profile"""
    return user.is_authenticated and hasattr(user, "placementstaff")


# Helper function to serialize drive object
def serialize_drive(drive, detailed=True):
    """Convert drive model instance to dictionary"""
    if detailed:
        # Full details for single drive view
        return {
            "id": drive.id,
            "company_name": drive.company_name,
            "point_of_contact": drive.point_of_contact,
            "year_of_passing": drive.year_of_passing,
            "job_received_date": (
                drive.job_received_date.isoformat() if drive.job_received_date else None
            ),
            "job_posted_date": (
                drive.job_posted_date.isoformat() if drive.job_posted_date else None
            ),
            "job_posted_by": drive.job_posted_by,
            "student_data_shared_date": (
                drive.student_data_shared_date.isoformat()
                if drive.student_data_shared_date
                else None
            ),
            "interview_date": (
                drive.interview_date.isoformat() if drive.interview_date else None
            ),
            "interview_posted_date": (
                drive.interview_posted_date.isoformat()
                if drive.interview_posted_date
                else None
            ),
            "results_declaration_status": drive.results_declaration_status,
            "results_declaration_date": (
                drive.results_declaration_date.isoformat()
                if drive.results_declaration_date
                else None
            ),
            "no_of_selects": drive.no_of_selects,
            "status": drive.status,
            "created_at": drive.created_at.isoformat(),
            "updated_at": drive.updated_at.isoformat(),
            "created_by": drive.created_by.username if drive.created_by else None,
            "updated_by": drive.updated_by.username if drive.updated_by else None,
        }
    else:
        # Basic details for list view
        return {
            "id": drive.id,
            "company_name": drive.company_name,
            "point_of_contact": drive.point_of_contact,
            "year_of_passing": drive.year_of_passing,
            "interview_date": (
                drive.interview_date.isoformat() if drive.interview_date else None
            ),
            "job_posted_by": drive.job_posted_by,
            "job_received_date": (
                drive.job_received_date.isoformat() if drive.job_received_date else None
            ),
            "results_declaration_status": drive.results_declaration_status,
            "status": drive.status,
        }


# List all drives or create a new drive
@csrf_exempt
def drive_list(request):
    """API endpoint for listing all drives or creating a new one"""
    if request.method == "GET":
        try:
            drives = CompanyDrive.objects.all().order_by("-created_at")
            return JsonResponse(
                {
                    "status": "success",
                    "count": drives.count(),
                    "drives": [
                        serialize_drive(drive, detailed=False) for drive in drives
                    ],
                }
            )
        except Exception as e:
            logger.error(f"Error fetching drives: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to fetch drives"}, status=500
            )

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            # Validate required fields
            required_fields = [
                "company_name",
                "point_of_contact",
                "year_of_passing",
                "job_received_date",
                "job_posted_date",
                "job_posted_by",
            ]
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": f"{field.replace('_', ' ').title()} is required",
                        },
                        status=400,
                    )

            # Create new drive
            drive = CompanyDrive(
                company_name=data.get("company_name"),
                point_of_contact=data.get("point_of_contact"),
                year_of_passing=int(data.get("year_of_passing")),
                job_received_date=datetime.strptime(
                    data.get("job_received_date"), "%Y-%m-%d"
                ).date(),
                job_posted_date=datetime.strptime(
                    data.get("job_posted_date"), "%Y-%m-%d"
                ).date(),
                job_posted_by=data.get("job_posted_by"),
            )

            # Set created_by if user is authenticated
            if hasattr(request, "user") and request.user.is_authenticated:
                drive.created_by = request.user

            # Optional fields
            if data.get("student_data_shared_date"):
                drive.student_data_shared_date = datetime.strptime(
                    data.get("student_data_shared_date"), "%Y-%m-%d"
                ).date()

            if data.get("interview_date"):
                drive.interview_date = datetime.strptime(
                    data.get("interview_date"), "%Y-%m-%d"
                ).date()

            if data.get("interview_posted_date"):
                drive.interview_posted_date = datetime.strptime(
                    data.get("interview_posted_date"), "%Y-%m-%d"
                ).date()

            if data.get("results_declaration_status"):
                drive.results_declaration_status = data.get(
                    "results_declaration_status"
                )

            if data.get("results_declaration_date"):
                drive.results_declaration_date = datetime.strptime(
                    data.get("results_declaration_date"), "%Y-%m-%d"
                ).date()

            if data.get("no_of_selects") is not None:
                drive.no_of_selects = int(data.get("no_of_selects"))

            drive.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Drive created successfully",
                    "drive": serialize_drive(drive),
                }
            )

        except ValueError as e:
            return JsonResponse(
                {"status": "error", "message": f"Invalid data format: {str(e)}"},
                status=400,
            )
        except Exception as e:
            logger.error(f"Error creating drive: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to create drive"}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


# Retrieve, update or delete a specific drive
@csrf_exempt
def drive_detail(request, drive_id):
    """API endpoint for retrieving, updating or deleting a specific drive"""
    try:
        drive = get_object_or_404(CompanyDrive, id=drive_id)
    except:
        return JsonResponse(
            {"status": "error", "message": "Drive not found"}, status=404
        )

    if request.method == "GET":
        return JsonResponse({"status": "success", "drive": serialize_drive(drive)})

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)

            # Update fields
            if "company_name" in data:
                drive.company_name = data.get("company_name")

            if "point_of_contact" in data:
                drive.point_of_contact = data.get("point_of_contact")

            if "year_of_passing" in data:
                drive.year_of_passing = int(data.get("year_of_passing"))

            if "job_received_date" in data and data.get("job_received_date"):
                drive.job_received_date = datetime.strptime(
                    data.get("job_received_date"), "%Y-%m-%d"
                ).date()

            if "job_posted_date" in data and data.get("job_posted_date"):
                drive.job_posted_date = datetime.strptime(
                    data.get("job_posted_date"), "%Y-%m-%d"
                ).date()

            if "job_posted_by" in data:
                drive.job_posted_by = data.get("job_posted_by")

            if "student_data_shared_date" in data:
                if data.get("student_data_shared_date"):
                    drive.student_data_shared_date = datetime.strptime(
                        data.get("student_data_shared_date"), "%Y-%m-%d"
                    ).date()
                else:
                    drive.student_data_shared_date = None

            if "interview_date" in data:
                if data.get("interview_date"):
                    drive.interview_date = datetime.strptime(
                        data.get("interview_date"), "%Y-%m-%d"
                    ).date()
                else:
                    drive.interview_date = None

            if "interview_posted_date" in data:
                if data.get("interview_posted_date"):
                    drive.interview_posted_date = datetime.strptime(
                        data.get("interview_posted_date"), "%Y-%m-%d"
                    ).date()
                else:
                    drive.interview_posted_date = None

            if "results_declaration_status" in data:
                drive.results_declaration_status = data.get(
                    "results_declaration_status"
                )

            if "results_declaration_date" in data:
                if data.get("results_declaration_date"):
                    drive.results_declaration_date = datetime.strptime(
                        data.get("results_declaration_date"), "%Y-%m-%d"
                    ).date()
                else:
                    drive.results_declaration_date = None

            if "no_of_selects" in data:
                if data.get("no_of_selects") is not None:
                    drive.no_of_selects = int(data.get("no_of_selects"))
                else:
                    drive.no_of_selects = None

            # Set updated_by if user is authenticated
            if hasattr(request, "user") and request.user.is_authenticated:
                drive.updated_by = request.user

            drive.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Drive updated successfully",
                    "drive": serialize_drive(drive),
                }
            )

        except ValueError as e:
            return JsonResponse(
                {"status": "error", "message": f"Invalid data format: {str(e)}"},
                status=400,
            )
        except Exception as e:
            logger.error(f"Error updating drive: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to update drive"}, status=500
            )

    elif request.method == "DELETE":
        try:
            company_name = drive.company_name
            drive.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"Drive for {company_name} deleted successfully",
                }
            )
        except Exception as e:
            logger.error(f"Error deleting drive: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to delete drive"}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


# List drives in progress
def drives_in_progress(request):
    """API endpoint for listing drives in progress"""
    if request.method == "GET":
        try:
            drives = CompanyDrive.objects.filter(status="IN_PROGRESS").order_by(
                "-created_at"
            )

            result = []
            for drive in drives:
                result.append(
                    {
                        "id": drive.id,
                        "company_name": drive.company_name,
                        "point_of_contact": drive.point_of_contact,
                        "interview_date": (
                            drive.interview_date.isoformat()
                            if drive.interview_date
                            else None
                        ),
                        "job_posted_by": drive.job_posted_by,
                        "results_declaration_status": drive.results_declaration_status,
                    }
                )

            return JsonResponse(
                {
                    "status": "success",
                    "count": len(result),
                    "drives_in_progress": result,
                }
            )
        except Exception as e:
            logger.error(f"Error fetching in-progress drives: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to fetch in-progress drives"},
                status=500,
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


# List pending drives
def pending_drives(request):
    """API endpoint for listing pending drives"""
    if request.method == "GET":
        try:
            drives = CompanyDrive.objects.filter(status="PENDING").order_by(
                "-created_at"
            )

            result = []
            for drive in drives:
                result.append(
                    {
                        "id": drive.id,
                        "company_name": drive.company_name,
                        "point_of_contact": drive.point_of_contact,
                        "year_of_passing": drive.year_of_passing,
                        "job_received_date": (
                            drive.job_received_date.isoformat()
                            if drive.job_received_date
                            else None
                        ),
                        "job_posted_by": drive.job_posted_by,
                        "results_declaration_status": drive.results_declaration_status,
                    }
                )

            return JsonResponse(
                {"status": "success", "count": len(result), "pending_drives": result}
            )
        except Exception as e:
            logger.error(f"Error fetching pending drives: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to fetch pending drives"},
                status=500,
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


# List completed drives
def completed_drives(request):
    """API endpoint for listing completed drives"""
    if request.method == "GET":
        try:
            drives = CompanyDrive.objects.filter(status="COMPLETED").order_by(
                "-created_at"
            )

            result = []
            for drive in drives:
                result.append(
                    {
                        "id": drive.id,
                        "company_name": drive.company_name,
                        "point_of_contact": drive.point_of_contact,
                        "interview_date": (
                            drive.interview_date.isoformat()
                            if drive.interview_date
                            else None
                        ),
                        "results_declaration_date": (
                            drive.results_declaration_date.isoformat()
                            if drive.results_declaration_date
                            else None
                        ),
                        "no_of_selects": drive.no_of_selects,
                    }
                )

            return JsonResponse(
                {"status": "success", "count": len(result), "completed_drives": result}
            )
        except Exception as e:
            logger.error(f"Error fetching completed drives: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to fetch completed drives"},
                status=500,
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )
