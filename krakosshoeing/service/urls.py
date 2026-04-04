from django.urls import path

from . import views

urlpatterns = [
    # User URLs
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),

    # Client URLs
    path("clients/", views.client_list, name="clients"),
    path("clients/new/", views.create_client, name="new_client"),
    path("clients/<int:client_id>/", views.client, name="client"),
    path("clients/<int:client_id>/edit/", views.edit_client, name="edit_client"),
    path("clients/<int:client_id>/delete/", views.delete_client, name="delete_client"),
    path("clients/<int:client_id>/horses/new/", views.add_client_horse, name="new_horse"),

    # Horse URLs
    path("horses/<int:horse_id>/edit/", views.edit_horse, name="edit_horse"),
    path("horses/<int:horse_id>/delete/", views.delete_horse, name="delete_horse"),

    # Job URLs
    path("jobs/new/", views.create_job, name="new_job"),
    path("jobs/<int:job_id>/", views.job, name="job"),
    path("jobs/<int:job_id>/edit/", views.edit_job, name="edit_job"),
    path("jobs/<int:job_id>/delete/", views.delete_job, name="delete_job"),
    path("jobs/<int:job_id>/item/new/", views.add_item, name="new_item"),
    path("jobs/<int:job_id>/receipt/", views.receipt, name="receipt"),

    # JobLineItem URLs
    path("item/<int:item_id>/edit/", views.edit_item, name="edit_item"),
    path("item/<int:item_id>/delete/", views.delete_item, name="delete_item")
]