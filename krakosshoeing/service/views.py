from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User, Client, Job, LineItem, Horse
from .forms import  RegistrationForm, LoginForm, ClientForm, HorseForm, JobForm, LineItemForm
    

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

            # Create a new user with the cleaned data
            user = User.objects.create_user(username=username, email=email, password=password)
            # Log in the new user
            login(request, user)
            # Display a success message to the user
            messages.success(request, "Registration successful! You are now logged in.")
            # Redirect the user to the dashboard
            return HttpResponseRedirect(reverse('service:dashboard'))
            
    # Otherwise
    else:
        # Create an empty form
        form = RegistrationForm()

    # Render the registration page with the form
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

    # Render the login page with the form
    return render(request, "service/login.html", {
        "form": form
    })
    

def logout_view(request):
    # Log user out
    logout(request)
    # Redirect user to the login page
    return HttpResponseRedirect(reverse("service:login"))


def logout_view(request):
    # Log user out
    logout(request)
    # Redirect user to the login page
    return HttpResponseRedirect(reverse("service:login"))


@login_required
def dashboard(request):
    
    # Get the next appointment
    # JOIN the Job and Client model 
    next_appointment = Job.objects.select_related('client').filter(
        # Filter by Jobs that have an upcoming appointment
        # WHERE Jobs are NOT NULL
        next_appointment__isnull=False,
        # WHERE upcoming appointments are >= to today's date
        next_appointment__gte=timezone.now().date(),
        # WHERE is_active is true
        is_active=True
    # ORDER BY upcoming appointment date and get the first result
    ).order_by('next_appointment').first()

    # If there is an upcoming appointment
    if next_appointment:
        # Get all horses related to the owner(client) of the upcoming appointment
        # JOIN the Horse and Client model
        appointment_horses = Horse.objects.select_related('owner').filter(
            # Filter by horses that are owned by the client of the upcoming appointment
            # WHERE owner = client of the upcoming appointment
            owner=next_appointment.client,
            # WHERE is_active is true
            is_active=True
        )

        # Get the last visit for the client of the upcoming appointment
        # JOIN the Job and Client model
        last_visit = Job.objects.select_related('client').filter(
            # Filter by jobs that are related to the client of the upcoming appointment
            # WHERE client = client of the upcoming appointment
            client=next_appointment.client,
            # WHERE is_active is true
            is_active=True
        # ORDER BY date and get the first result
        ).order_by('-date').first()

    # Otherwise, if there is no upcoming appointment
    else:
        # Set appointment_horses to None
        appointment_horses = None
        # Set last_visit to None
        last_visit = None

    # If there is a last visit
    if last_visit:
        # Get all line items related to the last visit
        # JOIN the LineItem, Horse, and Service models
        last_visit_items = LineItem.objects.select_related(
            'horse', 'service'
        # Filter by line items that are related to the last visit
        ).filter(job=last_visit)

    # Otherwise, if there is no last visit
    else:
        # Set last_visit_items to None
        last_visit_items = None

    # Get the 5 most recent jobs
    # JOIN the Job and Client model
    recent_jobs = Job.objects.select_related('client').filter(
        # Filter by jobs that are active
        # WHERE is_active is true
        is_active=True
    # ORDER BY date and get the first 5 results
    ).order_by('-date')[:5]

    # Get the total number of active clients
    # Filter the Client model by active clients and get the count
    total_clients = Client.objects.filter(is_active=True).count()

    # Render the dashboard page
    # with the next appointment, appointment horses, last visit, last visit items, recent jobs, and total clients
    return render(request, "service/dashboard.html", {
        "next_appointment": next_appointment,
        "appointment_horses": appointment_horses,
        "last_visit": last_visit,
        "last_visit_items": last_visit_items,
        "recent_jobs": recent_jobs,
        "total_clients": total_clients,
    })


@login_required
def create_client(request):
    # If the user submits the create client form
    if request.method == "POST":

        # Pass the submitted data and files to the form
        form = ClientForm(request.POST, request.FILES)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(request, "Client successfully created!")
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
    
    # Render client list page with all active clients
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

    # Render client page with the client, their jobs, and their horses
    return render(request, "service/client.html", {
        "client": client,
        "jobs": jobs,
        "horses": horses
    })


@login_required
def edit_client(request, client_id):
    # Get client by id
    client = get_object_or_404(Client, pk=client_id)

    # If the user submits the edit client form
    if request.method == "POST":

        # Pass the submitted data and files to the form
        form = ClientForm(request.POST, request.FILES, instance=client)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(request, f"{client.first_name}'s information successfully updated!")
            # Redirect the user to the client list page
            return HttpResponseRedirect(reverse('service:clients'))
        
    # Otherwise
    else:
        # Create a form pre-filled with the client's current information
        form = ClientForm(instance=client)

    # Render the edit client page with the form
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
        messages.success(request, f"{client.first_name} is deactivated. All records have been retained.")
        # Redirect the user to the client list page
        return HttpResponseRedirect(reverse('service:clients'))
    
    # Render the delete client page
    return render(request, "service/delete_client.html", {
        "client": client
    })


@login_required
def add_client_horse(request, client_id):
    # Get client by id
    client = get_object_or_404(Client, pk=client_id)

    # If the user submits the add horse form
    if request.method == "POST":
        # Pass the submitted data and files to the form
        form = HorseForm(request.POST, request.FILES)

        # If the form is valid
        if form.is_valid():
            # Create, but don't save the new horse instance.
            horse = form.save(commit=False)
            # Set the horse's owner to the client
            horse.owner = client
            # Save the horse to the database
            horse.save()
            # Display a success message to the user
            messages.success(request, f'The Horse was successfully added to {client.first_name}!')
            # Redirect the user to the client page
            return HttpResponseRedirect(reverse('service:client', args=[client_id]))
        
    # Otherwise
    else:
        # Create an empty form
        form = HorseForm()

    # Render the add client horse page with the form and client
    return render(request, "service/add_client_horse.html", {
        "form": form
    })


@login_required
def edit_horse(request, horse_id):
    # Get horse by id
    horse = get_object_or_404(Horse, pk=horse_id)
    # Get the client id from the horse's owner field
    client = horse.owner.id

    # If the user submits the edit horse form
    if request.method == "POST":

        # Pass the submitted data and files to the form
        form = HorseForm(request.POST, request.FILES, instance=horse)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(request, f"{horse.name}'s information successfully updated!")
            # Redirect the user to the client list page
            return HttpResponseRedirect(reverse('service:client', args=[client]))
    
    # Otherwise
    else:
        # Create a form pre-filled with the horse's current information
        form = HorseForm(instance=horse)
        
    # Render the edit horse page
    return render(request, "service/edit_horse.html", {
        "form": form
    })


@login_required
def delete_horse(request, horse_id):
    # Get horse by id
    horse = get_object_or_404(Horse, pk=horse_id)
    # Get the client id from the horse's owner field
    client = horse.owner.id

    # If the user submits the delete horse form
    if request.method == "POST":
        # Set the horses is_active field to False to soft delete the horse
        horse.is_active = False
        # Save the changes to the horse
        horse.save()
        # Display a success message to the user
        messages.success(request, f"{horse.name} is deactivated. All records have been retained.")
        # Redirect the user to the client page
        return HttpResponseRedirect(reverse('service:client', args=[client]))
    
    # Render the delete horse page
    return render(request, "service/delete_horse.html", {
        "horse": horse
    })


@login_required
def create_job(request):
    # If the user submits the create job form
    if request.method == "POST":

        # Pass the submitted data to the form
        form = JobForm(request.POST)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Get the id of the newly created job
            job = form.instance.id
            # Display a success message to the user
            messages.success(request, f"Job successfully created!")
            # Redirect the user to the job page
            return HttpResponseRedirect(reverse('service:job', args=[job]))

    # Otherwise 
    else:
        # Create an empty form
        form = JobForm()

    # Render the create job page with the form
    return render(request, "service/create_job.html", {
        "form": form
    })


@login_required
def job(request, job_id):
    # Get job by id
    job = get_object_or_404(Job, pk=job_id)
    # Get the client related to the job
    client = job.client

    # Render the job page with the job and client
    return render(request, "service/job.html", {
        "job": job,
        "client": client
    })


@login_required
def edit_job(request, job_id):
    # Get job by id
    job = get_object_or_404(Job, pk=job_id)

    # If the user submits the edit job form
    if request.method == "POST":

        # Pass the submitted data to the form, along with the instance of the job being edited
        form = JobForm(request.POST, instance=job)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(request, f"Job successfully updated!")
            # Redirect the user to the job page
            return HttpResponseRedirect(reverse('service:job', args=[job_id]))

    # Otherwise 
    else:
        # Create a form pre-filled with the job's current information
        form = JobForm(instance=job)

    # Render the edit job page with the form
    return render(request, "service/edit_job.html", {
        "form": form
    })


@login_required
def delete_job(request, job_id):
    # Get job by id
    job = get_object_or_404(Job, pk=job_id)
    # Get all line items related to the job
    item = LineItem.objects.filter(job=job)
    # Get the client id from the job's client field
    client = job.client.id

    # If the user submits the delete job form
    if request.method == "POST":

        # If there are line items related to the job
        if item:
            # Set the job is_active field to False to soft delete the job
            job.is_active = False
            # Save the changes to the job
            job.save()
            # Display a success message to the user
            messages.success(request, f"Job is deactivated. All records have been retained.")
            # Redirect the user to the client page
            return HttpResponseRedirect(reverse('service:client', args=[client]))
        
        # Otherwise, if there are no line items related to the job
        else:
            # permanently deleted the job
            job.delete()
            # Display a success message to the user
            messages.success(request, f"Job has been permanently deleted")
            # Redirect the user to the client page
            return HttpResponseRedirect(reverse('service:client', args=[client]))
    
    # Render the delete job page
    return render(request, "service/delete_job.html", {
        "job": job,
        "item": item,
    })


@login_required
def add_item(request, job_id):
    # Get job by id
    job = get_object_or_404(Job, pk=job_id)
    # Get the client from the job's client field
    client = job.client

    # If the user submits the add item form
    if request.method == "POST":

        # Pass the submitted data to the form
        form = LineItemForm(request.POST, client=client)

        # If the form is valid
        if form.is_valid():
            # Create, but don't save the new line item instance.
            item = form.save(commit=False)
            # Set the line item's job to the current job
            item.job = job
            # Save the line item to the database
            item.save()
            # Display a success message to the user
            messages.success(request, f"Item successfully added!")
            # Redirect the user to the job page
            return HttpResponseRedirect(reverse('service:job', args=[job_id]))
        
    # Otherwise
    else:
        # Create an empty form
        form = LineItemForm(client=client)

    # Render the add item page with the form
    return render(request, "service/add_item.html", {
        "form": form
    })


@login_required
def edit_item(request, item_id):
    # Get line item by id
    item = get_object_or_404(LineItem, pk=item_id)
    # Get the job id from the line item's job field
    job = item.job.id
    # Get the client from the job's client field
    client = job.client

    # If the user submits the edit item form
    if request.method == "POST":

        # Pass the submitted data to the form, along with the instance of the line item being edited
        form = LineItemForm(request.POST, instance=item, client=client)

        # If the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(request, f"Item information successfully updated!")
            # Redirect the user to the job page
            return HttpResponseRedirect(reverse('service:job', args=[job]))
    
    # Otherwise
    else:
        # Create a form pre-filled with the line item's current information
        form = LineItemForm(instance=item, client=client)

    # Render the edit item page with the form
    return render(request, "service/edit_item.html", {
        "form": form
    })


@login_required
def delete_item(request, item_id):
    # Get line item by id
    item = get_object_or_404(LineItem, pk=item_id)
    # Get the job id from the line item's job field
    job = item.job.id

    # If the user submits the delete item form
    if request.method == "POST":
        # permanently delete the item
        item.delete()
        # Display a success message to the user
        messages.success(request, f"Item has been permanently deleted")
        # Redirect the user to the job page
        return HttpResponseRedirect(reverse('service:job', args=[job]))
    
    # Render the delete item page
    return render(request, "service/delete_item.html", {
        "item": item,
        "job": job
    })


@login_required
def receipt(request, job_id):
    # Get job by id
    job = get_object_or_404(Job, pk=job_id)
    # Get all line items for this job
    items = LineItem.objects.filter(job=job)
    # Get the total
    job_total = job.get_total()

    # Render the receipt template
    return render(request, "service/receipt.html", {
        "job": job,
        "items": items,
        "job_total": job_total
    })