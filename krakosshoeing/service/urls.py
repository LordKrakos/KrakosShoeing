from django.urls import path

from . import views

urlpatterns = [
    # User URLs
    path('', views.dashboard, name="dashboard"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),

    # Client URLs
    path("clients", views.client_list, name="clients"),
    path("clients/<int:id>/", views.client, name="client"),
    path("clients/new/", views.create_client, name="new client")

    # Horse URLs

    # Job URLs

    # JobLineItem URLs
]