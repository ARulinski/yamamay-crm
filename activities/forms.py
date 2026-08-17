from django import forms

from .models import Interaction


class InteractionForm(forms.ModelForm):

    create_follow_up = forms.BooleanField(
        required=False,
        label="Create follow-up",
    )

    follow_up_title = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. Call about new collection",
            }
        ),
    )

    follow_up_type = forms.ChoiceField(
        required=False,
        choices=[
            ("call", "Call"),
            ("email", "Email"),
            ("whatsapp", "WhatsApp"),
            ("appointment", "Appointment"),
            ("store_visit", "Store Visit"),
            ("other", "Other"),
        ],
    )

    follow_up_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date"}
        ),
    )

    follow_up_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={"type": "time"}
        ),
    )

    class Meta:
        model = Interaction

        fields = [
            "interaction_type",
            "notes",

            "appointment_date",
            "appointment_time",
            "appointment_duration",
            "appointment_purpose",
            "appointment_location",

            "purchase_date",
            "purchase_value",
            "purchase_category",
            "purchase_quantity",
            "purchase_store",
            "purchase_reference",
        ]

        widgets = {

            "notes": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "What happened during this interaction?",
                }
            ),

            "appointment_date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "appointment_time": forms.TimeInput(
                attrs={"type": "time"}
            ),

            "appointment_duration": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 45",
                    "min": 1,
                }
            ),

            "appointment_purpose": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Fitting / VIP appointment",
                }
            ),

            "appointment_location": forms.TextInput(
                attrs={
                    "placeholder": "Store / Location",
                }
            ),

            "purchase_date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "purchase_value": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "purchase_quantity": forms.NumberInput(
                attrs={
                    "placeholder": "1",
                    "min": 1,
                }
            ),

            "purchase_store": forms.TextInput(
                attrs={
                    "placeholder": "Store",
                }
            ),

            "purchase_reference": forms.TextInput(
                attrs={
                    "placeholder": "Receipt / Order reference",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        interaction_type = cleaned_data.get(
            "interaction_type"
        )

        # Appointment validation

        if interaction_type == "appointment":

            if not cleaned_data.get("appointment_date"):
                self.add_error(
                    "appointment_date",
                    "Select an appointment date.",
                )

            if not cleaned_data.get("appointment_time"):
                self.add_error(
                    "appointment_time",
                    "Select an appointment time.",
                )

        # Purchase validation

        if interaction_type == "purchase":

            if not cleaned_data.get("purchase_date"):
                self.add_error(
                    "purchase_date",
                    "Select a purchase date.",
                )

            if cleaned_data.get("purchase_value") is None:
                self.add_error(
                    "purchase_value",
                    "Enter the purchase value.",
                )

        # Follow-up validation

        if cleaned_data.get("create_follow_up"):

            if not cleaned_data.get("follow_up_title"):
                self.add_error(
                    "follow_up_title",
                    "Enter a follow-up title.",
                )

            if not cleaned_data.get("follow_up_date"):
                self.add_error(
                    "follow_up_date",
                    "Select a follow-up date.",
                )

        return cleaned_data