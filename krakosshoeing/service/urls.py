from django.urls import path

from . import views

urlpatterns = [
    # User URLs
    path('', views.dashboard, name="dashboard"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),

    # Client URLs
    path("clients", views.client_list, name="clients"),
    path("clients/new/", views.create_client, name="new_client"),
    path("clients/<int:client_id>/", views.client, name="client"),
    path("clients/<int:client_id>/edit/", views.edit_client, name="edit_client"),
    path("clients/<int:client_id>/delete/", views.delete_client, name="delete_client"),
    path("clients/<int:client_id>/horses/new/", views.add_client_horse, name="new_horse"),

    # Horse URLs

    # Job URLs

    # JobLineItem URLs
]