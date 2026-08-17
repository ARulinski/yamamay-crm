from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import CustomerForm
from .models import Customer


@login_required
def customer_list(request):

    customers = Customer.objects.all()

    query = request.GET.get(
        "q",
        "",
    ).strip()

    if query:

        customers = customers.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(postcode__icontains=query)
            | Q(city__icontains=query)
        )

    context = {
        "customers": customers,
        "query": query,
    }

    return render(
        request,
        "customers/customer_list.html",
        context,
    )


@login_required
def customer_detail(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk,
    )

    # --------------------------------------------------
    # ALL INTERACTIONS
    # --------------------------------------------------

    interactions = (
        customer.interactions
        .select_related(
            "created_by"
        )
        .all()
        .order_by(
            "-created_at"
        )
    )

    # --------------------------------------------------
    # FOLLOW UPS
    # --------------------------------------------------

    follow_ups = (
        customer.follow_ups
        .select_related(
            "assigned_to"
        )
        .filter(
            status="pending"
        )
        .order_by(
            "due_date",
            "due_time",
        )
    )

    # --------------------------------------------------
    # APPOINTMENTS
    # --------------------------------------------------

    appointments = (
        customer.interactions
        .filter(
            interaction_type="appointment"
        )
        .select_related(
            "created_by"
        )
        .order_by(
            "-appointment_date",
            "-appointment_time",
        )
    )

    # --------------------------------------------------
    # PURCHASES
    # --------------------------------------------------

    purchases = (
        customer.interactions
        .filter(
            interaction_type="purchase"
        )
        .select_related(
            "created_by"
        )
        .order_by(
            "-purchase_date",
            "-created_at",
        )
    )

    # --------------------------------------------------
    # CUSTOMER VALUE
    # --------------------------------------------------

    purchase_summary = purchases.aggregate(
        total_spend=Sum(
            "purchase_value"
        ),
        purchase_count=Count(
            "id"
        ),
        average_spend=Avg(
            "purchase_value"
        ),
    )

    total_spend = (
        purchase_summary["total_spend"]
        or 0
    )

    purchase_count = (
        purchase_summary["purchase_count"]
        or 0
    )

    average_spend = (
        purchase_summary["average_spend"]
        or 0
    )

    latest_purchase = purchases.first()

    context = {
        "customer": customer,

        "interactions": interactions,
        "follow_ups": follow_ups,
        "appointments": appointments,
        "purchases": purchases,

        "total_spend": total_spend,
        "purchase_count": purchase_count,
        "average_spend": average_spend,
        "latest_purchase": latest_purchase,
    }

    return render(
        request,
        "customers/customer_detail.html",
        context,
    )


@login_required
def customer_create(request):

    if request.method == "POST":

        form = CustomerForm(
            request.POST
        )

        if form.is_valid():

            customer = form.save(
                commit=False
            )

            customer.assigned_to = (
                request.user
            )

            customer.save()

            return redirect(
                "customer_detail",
                pk=customer.pk,
            )

    else:

        form = CustomerForm()

    return render(
        request,
        "customers/customer_form.html",
        {
            "form": form,
        },
    )