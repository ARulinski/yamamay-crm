from django.urls import path

from . import views


urlpatterns = [

    # ======================================================
    # FOLLOW-UP LIST
    # ======================================================

    path(
        "",
        views.follow_up_list,
        name="follow_up_list",
    ),

    # ======================================================
    # FOLLOW-UP DETAIL
    # ======================================================

    path(
        "<int:pk>/",
        views.follow_up_detail,
        name="follow_up_detail",
    ),

]