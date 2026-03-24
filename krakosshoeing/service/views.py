from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Client, Job, JobLineItem, Service, Horse
from .forms import ClientForm, JobForm, HorseForm
    

# Create your views here.
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
            return HttpResponseRedirect(reverse('serviceforms:clients'))
        
    # Otherwise
    else:
        # Create an empty form
        form = ClientForm()

    # Render the create_client.html template with the form
    return render(request, "serviceforms/create_client.html", {
        "form": form
    })


def client_list(request):
    # Get all clients and order them by last_name, first_name
    clients = Client.objects.all().order_by('last_name', 'first_name')
    
    # Render clients.html with all clients
    return render(request, "serviceforms/clients.html", {
        "clients": clients
    })


def client(request, client_id):
    # Get client by id
    client = get_object_or_404(Client, pk=client_id)
    jobs = Job.objects.filter(client=client)
    horses = Horse.objects.filter(owner=client)

    return render(request, "serviceforms/client.html", {
        "client": client,
        "jobs": jobs,
        "horses": horses
    })