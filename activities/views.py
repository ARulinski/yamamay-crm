from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone

from customers.models import Customer
from tasks.models import FollowUp

from .forms import InteractionForm
from .models import Interaction


@login_required
def interaction_create(request, customer_id):

    customer = get_object_or_404(
        Customer,
        pk=customer_id,
    )

    if request.method == "POST":

        form = InteractionForm(request.POST)

        if form.is_valid():

            interaction = form.save(commit=False)

            interaction.customer = customer
            interaction.created_by = request.user

            interaction.save()

            # --------------------------------------------------
            # OPTIONAL FOLLOW-UP
            # --------------------------------------------------

            if form.cleaned_data.get(
                "create_follow_up"
            ):

                FollowUp.objects.create(
                    customer=customer,
                    title=form.cleaned_data[
                        "follow_up_title"
                    ],
                    follow_up_type=(
                        form.cleaned_data[
                            "follow_up_type"
                        ]
                        or "call"
                    ),
                    due_date=form.cleaned_data[
                        "follow_up_date"
                    ],
                    due_time=form.cleaned_data[
                        "follow_up_time"
                    ],
                    assigned_to=request.user,
                )

            return redirect(
                "customer_detail",
                pk=customer.pk,
            )

    else:

        form = InteractionForm()

    return render(
        request,
        "activities/interaction_form.html",
        {
            "form": form,
            "customer": customer,
        },
    )


@login_required
def appointment_list(request):

    today = timezone.localdate()

    selected_filter = request.GET.get(
        "range",
        "today",
    )

    appointments = (
        Interaction.objects
        .filter(
            interaction_type="appointment",
        )
        .select_related(
            "customer",
            "created_by",
        )
    )

    # --------------------------------------------------
    # TODAY
    # --------------------------------------------------

    if selected_filter == "today":

        appointments = appointments.filter(
            appointment_date=today,
        )

    # --------------------------------------------------
    # TOMORROW
    # --------------------------------------------------

    elif selected_filter == "tomorrow":

        appointments = appointments.filter(
            appointment_date=(
                today + timedelta(days=1)
            ),
        )

    # --------------------------------------------------
    # NEXT 7 DAYS
    # --------------------------------------------------

    elif selected_filter == "week":

        appointments = appointments.filter(
            appointment_date__gte=today,
            appointment_date__lte=(
                today + timedelta(days=7)
            ),
        )

    # --------------------------------------------------
    # NEXT 30 DAYS
    # --------------------------------------------------

    elif selected_filter == "month":

        appointments = appointments.filter(
            appointment_date__gte=today,
            appointment_date__lte=(
                today + timedelta(days=30)
            ),
        )

    # --------------------------------------------------
    # PAST
    # --------------------------------------------------

    elif selected_filter == "past":

        appointments = appointments.filter(
            appointment_date__lt=today,
        ).order_by(
            "-appointment_date",
            "-appointment_time",
        )

    # --------------------------------------------------
    # ALL UPCOMING
    # --------------------------------------------------

    else:

        selected_filter = "all"

        appointments = appointments.filter(
            appointment_date__gte=today,
        )

    if selected_filter != "past":

        appointments = appointments.order_by(
            "appointment_date",
            "appointment_time",
        )

    context = {
        "appointments": appointments,
        "selected_filter": selected_filter,
        "today": today,
    }

    return render(
        request,
        "activities/appointment_list.html",
        context,
    )


@login_required
def appointment_detail(request, pk):

    appointment = get_object_or_404(
        Interaction.objects.select_related(
            "customer",
            "created_by",
        ),
        pk=pk,
        interaction_type="appointment",
    )

    context = {
        "appointment": appointment,
        "customer": appointment.customer,
    }

    return render(
        request,
        "activities/appointment_detail.html",
        context,
    )


@login_required
def purchase_detail(request, pk):

    purchase = get_object_or_404(
        Interaction.objects.select_related(
            "customer",
            "created_by",
        ),
        pk=pk,
        interaction_type="purchase",
    )

    context = {
        "purchase": purchase,
        "customer": purchase.customer,
    }

    return render(
        request,
        "activities/purchase_detail.html",
        context,
    )