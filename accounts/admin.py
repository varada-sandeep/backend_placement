from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import StaffRank, PlacementStaff


class PlacementStaffInline(admin.StackedInline):
    model = PlacementStaff
    can_delete = False
    verbose_name_plural = "Placement Staff"


class CustomUserAdmin(UserAdmin):
    inlines = (PlacementStaffInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_staff_rank",
    )

    def get_staff_rank(self, obj):
        if hasattr(obj, "placementstaff"):
            return (
                obj.placementstaff.rank.name if obj.placementstaff.rank else "No Rank"
            )
        return "Not Staff"

    get_staff_rank.short_description = "Staff Rank"


class StaffRankAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "staff_count", "description")
    ordering = ("level",)

    def staff_count(self, obj):
        """Display the number of staff members with this rank"""
        return obj.placementstaff_set.count()

    staff_count.short_description = "Number of Staff"


class PlacementStaffAdmin(admin.ModelAdmin):
    list_display = ("user", "rank", "department", "contact_number", "is_active")
    list_filter = ("rank", "department", "is_active")
    search_fields = ("user__username", "user__email", "department")

    def get_queryset(self, request):
        """Optimize queryset by prefetching related objects"""
        return super().get_queryset(request).select_related("user", "rank")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Sort the rank dropdown by level in forms"""
        if db_field.name == "rank":
            kwargs["queryset"] = StaffRank.objects.order_by("level")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Unregister the default User admin and register our custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(StaffRank, StaffRankAdmin)
admin.site.register(PlacementStaff, PlacementStaffAdmin)
