from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):

    # ======================================================
    # CHOICES
    # ======================================================

    BIRTHDAY_DAYS = [
        ("", "Day"),
    ] + [
        (i, str(i))
        for i in range(1, 32)
    ]

    MONTHS = [
        ("", "Month"),
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    ]

    # ======================================================
    # OPTIONAL DATE FIELDS
    # ======================================================

    birthday_day = forms.TypedChoiceField(
        choices=BIRTHDAY_DAYS,
        required=False,
        coerce=int,
        empty_value=None,
    )

    birthday_month = forms.TypedChoiceField(
        choices=MONTHS,
        required=False,
        coerce=int,
        empty_value=None,
    )

    spouse_birthday_day = forms.TypedChoiceField(
        choices=BIRTHDAY_DAYS,
        required=False,
        coerce=int,
        empty_value=None,
    )

    spouse_birthday_month = forms.TypedChoiceField(
        choices=MONTHS,
        required=False,
        coerce=int,
        empty_value=None,
    )

    # ======================================================
    # META
    # ======================================================

    class Meta:

        model = Customer

        fields = [
            "salutation",

            "first_name",
            "last_name",

            "birthday_day",
            "birthday_month",

            "email",

            "country",
            "address_line_1",
            "address_line_2",
            "postcode",
            "city",

            "phone_country_code",
            "phone",
            "phone_type",

            "anniversary",

            "spouse_birthday_day",
            "spouse_birthday_month",

            "nationality",

            "preferred_store",

            "notes",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "First Name",
                    "autocomplete": "given-name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Last Name",
                    "autocomplete": "family-name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email Address",
                    "autocomplete": "email",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "placeholder": (
                        "Country / Region of Residence"
                    ),
                    "autocomplete": "country-name",
                }
            ),

            "address_line_1": forms.TextInput(
                attrs={
                    "placeholder": "Address line 1",
                    "autocomplete": "address-line1",
                }
            ),

            "address_line_2": forms.TextInput(
                attrs={
                    "placeholder": "Address line 2",
                    "autocomplete": "address-line2",
                }
            ),

            "postcode": forms.TextInput(
                attrs={
                    "placeholder": "Post code",
                    "autocomplete": "postal-code",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "City / Town",
                    "autocomplete": "address-level2",
                }
            ),

            "phone_country_code": forms.TextInput(
                attrs={
                    "placeholder": "+44",
                    "inputmode": "tel",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Phone",
                    "inputmode": "tel",
                    "autocomplete": "tel",
                }
            ),

            "anniversary": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "nationality": forms.TextInput(
                attrs={
                    "placeholder": "Nationality",
                }
            ),

            "preferred_store": forms.TextInput(
                attrs={
                    "placeholder": "Preferred Store",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Customer notes..."
                    ),
                    "rows": 4,
                }
            ),
        }

    # ======================================================
    # MAKE ALL CUSTOMER DETAILS OPTIONAL
    # ======================================================

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs,
        )

        for field in self.fields.values():
            field.required = False