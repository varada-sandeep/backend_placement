from django.urls import path
from . import views

urlpatterns = [
    # CRUD operations
    path("drives/", views.drive_list, name="drive-list"),
    path("drives/<int:drive_id>/", views.drive_detail, name="drive_detail"),
    # Special endpoints
    path("drives/in-progress/", views.drives_in_progress, name="drives_in_progress"),
    path("drives/pending/", views.pending_drives, name="pending_drives"),
    path("drives/completed/", views.completed_drives, name="completed_drives"),
]
