from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):

    BIRTHDAY_DAYS = [("", "Day")] + [
        (i, str(i)) for i in range(1, 32)
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

    birthday_day = forms.ChoiceField(
        choices=BIRTHDAY_DAYS,
        required=False,
    )

    birthday_month = forms.ChoiceField(
        choices=MONTHS,
        required=False,
    )

    spouse_birthday_day = forms.ChoiceField(
        choices=BIRTHDAY_DAYS,
        required=False,
    )

    spouse_birthday_month = forms.ChoiceField(
        choices=MONTHS,
        required=False,
    )

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
                    "placeholder": "First Name *",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Last Name *",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email Address",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "placeholder": "Country / Region of Residence",
                }
            ),

            "address_line_1": forms.TextInput(
                attrs={
                    "placeholder": "Address line 1",
                }
            ),

            "address_line_2": forms.TextInput(
                attrs={
                    "placeholder": "Address line 2",
                }
            ),

            "postcode": forms.TextInput(
                attrs={
                    "placeholder": "Post code",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "City / Town",
                }
            ),

            "phone_country_code": forms.TextInput(
                attrs={
                    "placeholder": "+44",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Phone",
                    "inputmode": "tel",
                }
            ),

            "anniversary": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "nationality": forms.TextInput(
                attrs={
                    "placeholder": "Nationality / Passport",
                }
            ),

            "preferred_store": forms.TextInput(
                attrs={
                    "placeholder": "Preferred Store",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "placeholder": "Customer notes...",
                    "rows": 4,
                }
            ),
        }