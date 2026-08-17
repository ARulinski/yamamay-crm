from django.conf import settings
from django.db import models


class Customer(models.Model):

    class Salutation(models.TextChoices):
        DR = "dr", "Dr."
        MISS = "miss", "Miss."
        MR = "mr", "Mr."
        MRS = "mrs", "Mrs."
        MS = "ms", "Ms."

    class PhoneType(models.TextChoices):
        MOBILE = "mobile", "Mobile"
        HOME = "home", "Home"
        WORK = "work", "Work"
        OTHER = "other", "Other"

    # ======================================================
    # PERSONAL INFORMATION
    # ======================================================

    salutation = models.CharField(
        max_length=10,
        choices=Salutation.choices,
        blank=True,
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    birthday_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    birthday_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    # ======================================================
    # ADDRESS
    # ======================================================

    country = models.CharField(
        max_length=100,
        default="United Kingdom",
        blank=True,
    )

    address_line_1 = models.CharField(
        max_length=255,
        blank=True,
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    postcode = models.CharField(
        max_length=20,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    # ======================================================
    # PHONE
    # ======================================================

    phone_country_code = models.CharField(
        max_length=10,
        default="+44",
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    phone_type = models.CharField(
        max_length=20,
        choices=PhoneType.choices,
        default=PhoneType.MOBILE,
        blank=True,
    )

    # ======================================================
    # IMPORTANT DATES
    # ======================================================

    anniversary = models.DateField(
        null=True,
        blank=True,
    )

    spouse_birthday_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    spouse_birthday_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    # ======================================================
    # ADDITIONAL PERSONAL INFORMATION
    # ======================================================

    nationality = models.CharField(
        max_length=100,
        blank=True,
    )

    # ======================================================
    # CRM INFORMATION
    # ======================================================

    preferred_store = models.CharField(
        max_length=150,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers",
    )

    # ======================================================
    # SYSTEM
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "first_name",
            "last_name",
        ]

    def __str__(self):
        return self.full_name

    # ======================================================
    # DISPLAY NAME
    # ======================================================

    @property
    def full_name(self):

        name_parts = []

        if self.salutation:
            name_parts.append(
                self.get_salutation_display()
            )

        if self.first_name:
            name_parts.append(
                self.first_name
            )

        if self.last_name:
            name_parts.append(
                self.last_name
            )

        if name_parts:
            return " ".join(name_parts)

        if self.phone:
            return self.full_phone_number

        if self.email:
            return self.email

        return "Unnamed Customer"

    # ======================================================
    # PHONE
    # ======================================================

    @property
    def full_phone_number(self):

        if not self.phone:
            return ""

        if self.phone_country_code:
            return (
                f"{self.phone_country_code} "
                f"{self.phone}"
            ).strip()

        return self.phone

    # ======================================================
    # BIRTHDAY
    # ======================================================

    @property
    def birthday_display(self):

        if (
            not self.birthday_day
            or not self.birthday_month
        ):
            return ""

        return (
            f"{self.birthday_day:02d}/"
            f"{self.birthday_month:02d}"
        )

    # ======================================================
    # SPOUSE BIRTHDAY
    # ======================================================

    @property
    def spouse_birthday_display(self):

        if (
            not self.spouse_birthday_day
            or not self.spouse_birthday_month
        ):
            return ""

        return (
            f"{self.spouse_birthday_day:02d}/"
            f"{self.spouse_birthday_month:02d}"
        )