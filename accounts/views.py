from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from django.conf import settings
from importlib import import_module

def is_staff(user):
    """Check if the user is authenticated and associated with a PlacementStaff profile"""
    return user.is_authenticated and hasattr(user, "placementstaff")

@csrf_exempt
def signin_view(request):
    """API endpoint for user login"""
    if request.method == "POST":
        # Manually load the session
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if session_key:
            try:
                engine = import_module(settings.SESSION_ENGINE)
                request.session = engine.SessionStore(session_key)
            except Exception as e:
                return JsonResponse(
                    {"status": "error", "message": f"Session loading failed: {str(e)}"},
                    status=400,
                )

        try:
            data = json.loads(request.body)
            username = data.get("email")
            password = data.get("password")
            print(f"Attempting login for user: {username}")  # Debugging lin

            user = authenticate(request, username=username, password=password)

            if user is not None and hasattr(user, "placementstaff"):
                login(request, user)
                # Return user details including staff rank
                staff = user.placementstaff
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Login successful",
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "staff_rank": {
                                "name": staff.rank.name if staff.rank else None,
                                "level": staff.rank.level if staff.rank else None,
                            },
                            "department": staff.department,
                        },
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid credentials or not authorized as placement staff",
                    },
                    status=401,
                )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Only POST method is allowed"}, status=405
    )


@csrf_exempt
def signout_view(request):
    """API endpoint for user logout"""
    if request.method == "POST":
        logout(request)
        return JsonResponse({"status": "success", "message": "Logout successful"})

    return JsonResponse(
        {"status": "error", "message": "Only POST method is allowed"}, status=405
    )


@csrf_exempt
@login_required
@user_passes_test(is_staff)
def check_auth_status(request):
    """API endpoint to check if user is authenticated and get user details"""
    user = request.user
    staff = user.placementstaff

    return JsonResponse(
        {
            "status": "success",
            "authenticated": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "staff_rank": {
                    "name": staff.rank.name if staff.rank else None,
                    "level": staff.rank.level if staff.rank else None,
                },
                "department": staff.department,
            },
        }
    )
