from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

from .models import User, Client, Job, JobLineItem, Service, Horse
from .forms import  RegistrationForm ,ClientForm, JobForm, HorseForm
    

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
                # Redirect the user to the dahsboard
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
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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


def client_list(request):
    # Get all clients and order them by last_name, first_name
    clients = Client.objects.all().order_by('last_name', 'first_name')
    
    # Render clients.html with all clients
    return render(request, "service/clients.html", {
        "clients": clients
    })


def client(request, client_id):
    # Get client by id
    client = get_object_or_404(Client, pk=client_id)
    jobs = Job.objects.filter(client=client)
    horses = Horse.objects.filter(owner=client)

    return render(request, "service/client.html", {
        "client": client,
        "jobs": jobs,
        "horses": horses
    })