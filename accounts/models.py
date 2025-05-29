from django.db import models
from django.contrib.auth.models import User, AbstractUser


class StaffRank(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Level {self.level})"

    class Meta:
        ordering = ["level"]
        verbose_name = "Staff Rank"
        verbose_name_plural = "Staff Ranks"

    def get_staff_count(self):
        """Returns the number of staff members with this rank"""
        return self.placementstaff_set.count()


class PlacementStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.ForeignKey(StaffRank, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.rank.name if self.rank else 'No Rank'}"
