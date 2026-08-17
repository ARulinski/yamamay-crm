from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "email",
        "full_phone_number",
        "city",
        "preferred_store",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "postcode",
        "city",
    )

    list_filter = (
        "salutation",
        "country",
        "phone_type",
        "preferred_store",
        "assigned_to",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Personal Information",
            {
                "fields": (
                    "salutation",
                    "first_name",
                    "last_name",
                    "birthday_day",
                    "birthday_month",
                    "email",
                    "nationality",
                )
            },
        ),

        (
            "Address",
            {
                "fields": (
                    "country",
                    "address_line_1",
                    "address_line_2",
                    "postcode",
                    "city",
                )
            },
        ),

        (
            "Phone",
            {
                "fields": (
                    "phone_country_code",
                    "phone",
                    "phone_type",
                )
            },
        ),

        (
            "Important Dates",
            {
                "fields": (
                    "anniversary",
                    "spouse_birthday_day",
                    "spouse_birthday_month",
                )
            },
        ),

        (
            "CRM",
            {
                "fields": (
                    "preferred_store",
                    "assigned_to",
                    "notes",
                )
            },
        ),

        (
            "System",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )