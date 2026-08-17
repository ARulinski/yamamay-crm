from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.utils import timezone

from .models import FollowUp


@login_required
def follow_up_list(request):

    today = timezone.localdate()

    selected_filter = request.GET.get(
        "range",
        "today",
    )

    follow_ups = (
        FollowUp.objects
        .select_related(
            "customer",
            "assigned_to",
        )
        .all()
    )

    # --------------------------------------------------
    # OVERDUE
    # --------------------------------------------------

    if selected_filter == "overdue":

        follow_ups = follow_ups.filter(
            status="pending",
            due_date__lt=today,
        )

    # --------------------------------------------------
    # TODAY
    # --------------------------------------------------

    elif selected_filter == "today":

        follow_ups = follow_ups.filter(
            status="pending",
            due_date=today,
        )

    # --------------------------------------------------
    # TOMORROW
    # --------------------------------------------------

    elif selected_filter == "tomorrow":

        follow_ups = follow_ups.filter(
            status="pending",
            due_date=today + timedelta(days=1),
        )

    # --------------------------------------------------
    # NEXT 7 DAYS
    # --------------------------------------------------

    elif selected_filter == "week":

        follow_ups = follow_ups.filter(
            status="pending",
            due_date__gte=today,
            due_date__lte=today + timedelta(days=7),
        )

    # --------------------------------------------------
    # NEXT 30 DAYS
    # --------------------------------------------------

    elif selected_filter == "month":

        follow_ups = follow_ups.filter(
            status="pending",
            due_date__gte=today,
            due_date__lte=today + timedelta(days=30),
        )

    # --------------------------------------------------
    # ALL PENDING
    # --------------------------------------------------

    elif selected_filter == "all":

        follow_ups = follow_ups.filter(
            status="pending",
        )

    # --------------------------------------------------
    # COMPLETED
    # --------------------------------------------------

    elif selected_filter == "completed":

        follow_ups = follow_ups.filter(
            status="completed",
        )

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    else:

        selected_filter = "today"

        follow_ups = follow_ups.filter(
            status="pending",
            due_date=today,
        )

    # --------------------------------------------------
    # ORDERING
    # --------------------------------------------------

    if selected_filter == "completed":

        follow_ups = follow_ups.order_by(
            "-due_date",
            "-due_time",
        )

    else:

        follow_ups = follow_ups.order_by(
            "due_date",
            "due_time",
        )

    context = {
        "follow_ups": follow_ups,
        "selected_filter": selected_filter,
        "today": today,
    }

    return render(
        request,
        "tasks/follow_up_list.html",
        context,
    )


@login_required
def follow_up_detail(request, pk):

    follow_up = get_object_or_404(
        FollowUp.objects.select_related(
            "customer",
            "assigned_to",
        ),
        pk=pk,
    )

    context = {
        "follow_up": follow_up,
        "customer": follow_up.customer,
    }

    return render(
        request,
        "tasks/follow_up_detail.html",
        context,
    )