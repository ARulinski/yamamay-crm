from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from activities.models import Interaction
from customers.models import Customer
from tasks.models import FollowUp


@login_required
def dashboard(request):

    now = timezone.localtime()
    today = now.date()

    # --------------------------------------------------
    # GREETING
    # --------------------------------------------------

    hour = now.hour

    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    # --------------------------------------------------
    # CUSTOMER COUNT
    # --------------------------------------------------

    customer_count = Customer.objects.count()

    # --------------------------------------------------
    # FOLLOW UPS
    # --------------------------------------------------

    pending_follow_up_count = FollowUp.objects.filter(
        status="pending",
    ).count()

    todays_follow_ups = (
        FollowUp.objects
        .filter(
            due_date=today,
            status="pending",
        )
        .select_related(
            "customer",
            "assigned_to",
        )
        .order_by(
            "due_time",
            "created_at",
        )
    )

    # --------------------------------------------------
    # APPOINTMENTS
    # --------------------------------------------------

    appointment_count = Interaction.objects.filter(
        interaction_type="appointment",
        appointment_date__gte=today,
    ).count()

    todays_appointments = (
        Interaction.objects
        .filter(
            interaction_type="appointment",
            appointment_date=today,
        )
        .select_related(
            "customer",
            "created_by",
        )
        .order_by(
            "appointment_time",
        )
    )

    # --------------------------------------------------
    # INTERACTIONS
    # --------------------------------------------------

    interaction_count = Interaction.objects.count()

    context = {
        "today": today,
        "greeting": greeting,

        "customer_count": customer_count,
        "pending_follow_up_count": pending_follow_up_count,
        "appointment_count": appointment_count,
        "interaction_count": interaction_count,

        "todays_follow_ups": todays_follow_ups,
        "todays_appointments": todays_appointments,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )