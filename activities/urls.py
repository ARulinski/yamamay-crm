from django.urls import path

from . import views


urlpatterns = [

    # APPOINTMENTS

    path(
        "appointments/",
        views.appointment_list,
        name="appointment_list",
    ),

    path(
        "appointments/<int:pk>/",
        views.appointment_detail,
        name="appointment_detail",
    ),


    # PURCHASES

    path(
        "purchases/<int:pk>/",
        views.purchase_detail,
        name="purchase_detail",
    ),


    # INTERACTIONS

    path(
        "customer/<int:customer_id>/new/",
        views.interaction_create,
        name="interaction_create",
    ),

]