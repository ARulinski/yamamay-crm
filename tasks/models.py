from django.conf import settings
from django.db import models


class FollowUp(models.Model):

    class FollowUpType(models.TextChoices):
        CALL = "call", "Call"
        EMAIL = "email", "Email"
        WHATSAPP = "whatsapp", "WhatsApp"
        APPOINTMENT = "appointment", "Appointment"
        STORE_VISIT = "store_visit", "Store Visit"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="follow_ups",
    )

    title = models.CharField(
        max_length=200,
    )

    follow_up_type = models.CharField(
        max_length=30,
        choices=FollowUpType.choices,
        default=FollowUpType.CALL,
    )

    due_date = models.DateField()

    due_time = models.TimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="follow_ups",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "due_date",
            "due_time",
        ]

    def __str__(self):
        return f"{self.customer.full_name} - {self.title}"