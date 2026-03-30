from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User, Client, Job, JobLineItem, Service, Horse
from .forms import  RegistrationForm, LoginForm, ClientForm, JobForm, HorseForm
    

# Create your views here.
def register(request):
    # If the user submits the registration form
    if request.method == "POST":

        # Pass the submitted data to the form
        form = RegistrationForm(request.POST)

        # If the form is valid
        if form.is_valid():
            # Get the cleaned data from the form
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Try to
            try:
                # Create a new user with the cleaned data
                user = User.objects.create_user(username=username, email=email, password=password)
                # Log in the new user
                login(request, user)
                # Display a success message to the user
                messages.success(request, 'Registration successful! You are now logged in.')
                # Redirect the user to the dashboard
                return HttpResponseRedirect(reverse('service:dashboard'))
            
            # Except if an IntegrityError is raised
            except IntegrityError:
                # Display an error message to the user
                messages.error(request, 'Username already taken. Please choose a different username.')
                # Redirect the user back to the registration page
                return render(request, "service/registration.html", {
                    "form": form
                })
            
    # Otherwise
    else:
        # Create an empty form
        form = RegistrationForm()

    # Render the registration.html template with the form
    return render(request, "service/registration.html", {
        "form": form
    })
    

def login_view(request):
    # If the user submits the login form
    if request.method == "POST":

        # Pass the submitted data to the form
        form = LoginForm(request.POST)

        # If the form is valid
        if form.is_valid():
            # Get the cleaned data from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            # If the user is authenticated
            if user is not None:
                # Log in the user
                login(request, user)
                # Display a success message to the user
                messages.success(request, "Login successful")
                # Redirect the user to the dashboard
                return HttpResponseRedirect(reverse("service:dashboard"))
            else:
                # Display an error message to the user
                messages.error(request, "Invalid username and/or password.")
                # Redirect the user back to the login page
                return render(request, "service/login.html", {
                    "form": form
                })
    
    # Otherwise
    else:
        # Create an empty form
        form = LoginForm()

    # Render the login.html template with the form
    return render(request, "service/login.html", {
        "form": form
    })
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("service:login"))


@login_required
# TODO: dashboard view


@login_required
def create_client(request):
    # If the user submits the form
    if request.method == "POST":

        # Pass the submitted data and files to the form
        form = ClientForm(request.POST, request.FILES)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(request, 'Client successfully created!')
            # Redirect the user to the client list page
            return HttpResponseRedirect(reverse('service:clients'))
        
    # Otherwise
    else:
        # Create an empty form
        form = ClientForm()

    # Render the create_client.html template with the form
    return render(request, "service/create_client.html", {
        "form": form
    })


@login_required
def client_list(request):
    # Get all active clients and order them by last_name, first_name
    clients = Client.objects.filter(is_active=True).order_by('last_name', 'first_name')
    
    # Render clients.html with all clients
    return render(request, "service/clients.html", {
        "clients": clients
    })


@login_required
def client(request, client_id):
    # Get client by id
    client = get_object_or_404(Client, pk=client_id)
    # Get all jobs related to the client
    jobs = Job.objects.filter(client=client)
    # Get all horses related to the client
    horses = Horse.objects.filter(owner=client)

    # Render client.html with the client, their jobs, and their horses
    return render(request, "service/client.html", {
        "client": client,
        "jobs": jobs,
        "horses": horses
    })


@login_required
def edit_client(request, client_id):
    # Get client by id
    client = get_object_or_404(Client, pk=client_id)

    # If the user submits the form
    if request.method == "POST":

        # Pass the submitted data and files to the form
        form = ClientForm(request.POST, request.FILES, instance=client)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(request, 'Client information successfully updated!')
            # Redirect the user to the client list page
            return HttpResponseRedirect(reverse('service:clients'))
        
    # Otherwise
    else:
        # Create a form pre-filled with the client's current information
        form = ClientForm(instance=client)

    # Render the edit_client.html template with the form
    return render(request, "service/edit_client.html", {
        "form": form
    })
        

@login_required
def delete_client(request, client_id):
    # Get client by id
    client = get_object_or_404(Client, pk=client_id)
    
    # If the user submits the delete client form
    if request.method == "POST":
        # Set the client's is_active field to False to soft delete the client
        client.is_active = False
        # Save the changes to the client
        client.save()
        # Display a success message to the user
        messages.success(request, 'Client deactivated. All records have been retained.')
        # Redirect the user to the client list page
        return HttpResponseRedirect(reverse('service:clients'))
    
    # Render the delete_client.html template
    return render(request, "service/delete_client.html", {
        "client": client
    })


@login_required
def add_client_horse(request):
    if request.method == "POST":

        form = HorseForm(request.POST)

        if form.is_valid:
            form.save()
            messages.success(request, 'Horse successfully added to client!')
            return HttpResponseRedirect(reverse('service:client'))
        
    else:
        form = HorseForm()

    return render(request, "service/add_client_horse.html", {
        "form": form
    })