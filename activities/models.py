from django.conf import settings
from django.db import models


class Interaction(models.Model):

    class InteractionType(models.TextChoices):
        STORE_VISIT = "store_visit", "Store Visit"
        CALL = "call", "Phone Call"
        EMAIL = "email", "Email"
        WHATSAPP = "whatsapp", "WhatsApp"
        APPOINTMENT = "appointment", "Appointment"
        PURCHASE = "purchase", "Purchase"
        OTHER = "other", "Other"

    class PurchaseCategory(models.TextChoices):
        LINGERIE = "lingerie", "Lingerie"
        NIGHTWEAR = "nightwear", "Nightwear"
        SWIMWEAR = "swimwear", "Swimwear"
        CLOTHING = "clothing", "Clothing"
        ACCESSORIES = "accessories", "Accessories"
        OTHER = "other", "Other"

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    interaction_type = models.CharField(
        max_length=30,
        choices=InteractionType.choices,
    )

    notes = models.TextField(
        blank=True,
    )

    # --------------------------------------------------
    # APPOINTMENT
    # --------------------------------------------------

    appointment_date = models.DateField(
        null=True,
        blank=True,
    )

    appointment_time = models.TimeField(
        null=True,
        blank=True,
    )

    appointment_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration in minutes",
    )

    appointment_purpose = models.CharField(
        max_length=150,
        blank=True,
    )

    appointment_location = models.CharField(
        max_length=150,
        blank=True,
    )

    # --------------------------------------------------
    # PURCHASE
    # --------------------------------------------------

    purchase_date = models.DateField(
        null=True,
        blank=True,
    )

    purchase_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    purchase_category = models.CharField(
        max_length=30,
        choices=PurchaseCategory.choices,
        blank=True,
    )

    purchase_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    purchase_store = models.CharField(
        max_length=150,
        blank=True,
    )

    purchase_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    # --------------------------------------------------
    # SYSTEM
    # --------------------------------------------------

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_interactions",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.customer.full_name} - "
            f"{self.get_interaction_type_display()}"
        )