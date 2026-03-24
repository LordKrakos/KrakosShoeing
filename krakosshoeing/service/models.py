from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    pass


class Client(models.Model):
    """
    Represents a client who receives shoeing services.

    Model Fields:
        - first_name: The client's first name (max length 100 characters).
        - last_name: The client's last name (max length 100 characters).
        - photo: An optional image field for the client's photo, uploaded to 'client_photos/'.
        - business_name: The client's business name (max length 100 characters).
        - phone_number: The client's phone number, stored using the PhoneNumberField from the django-phonenumber-field package.
        - email: The client's email address (max length 254 characters).

    String Representation:
        - If the client is related to a business, it returns "FirstName LastName - BusinessName".
        - Otherwise, it returns "FirstName LastName".
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='client_photos/', blank=True, null=True)
    business_name = models.CharField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        if self.business_name:
            return f"{self.first_name} {self.last_name} - {self.business_name}"
        return f"{self.first_name} {self.last_name}"


class Service(models.Model):
    """
    Represents a shoeing service.

    Model Fields:
        - name: The name of the service, chosen from a predefined list of options.
        - price: The price of the service, stored as a decimal with up to 8 digits and 2 decimal places.

    String Representation:
        - Returns a string in the format of the service "Name - Price".
    """

    class Services(models.TextChoices):
        DEFAULT = "--", _("-------")
        FULL_TRIM = "FTRM", _("Full Trim")
        SHOE_FR_TRIM_BK = "SFTB", _("Shoe Front/Trim Back")
        FULL_SHOES = "FS", _("Full Shoes")
        STEEL = "ST", _("Steel Shoes")
        ALUMINUM = "ALU", _("Aluminum Shoes")
        PADS = "PAD", _("Pad(s)")
        PACKING = "PAC", _("Packing")
        CLIPS = "CL", _("Clip(s)")
        ROCKER_TOES = "ROKT", _("Rocker Toe(s)")
        ROLLED_TOES = "ROLT", _("Rolled Toe(s)")
        SQUARE_TOES = "SQT", _("Square Toe(s)")
        TRAILERS = "TRL", _("Trailer(s)")
        EGG_BARS = "EB", _("Egg Bar(s)")
        STRAIGHT_BARS = "SB", _("Straight Bar(s)")
        HOOF_REPAIRS = "HR", _("Hoof Repair(s)")

    name = models.CharField(
        max_length=4,
        choices=Services,
        default=Services.DEFAULT
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.get_name_display()} - {self.price}"


class Horse(models.Model):
    """
    Represents a horse owned by a client.

    Model Fields:
        - owner: A foreign key linking to the Client model, representing the horse's owner.
        - name: The name of the horse (max length 100 characters).
        - breed: The breed of the horse (max length 100 characters).
        - photo: An optional image field for the horse's photo, uploaded to 'horse_photos/'.
        - description: A text field for additional details about the horse (max length 3000 characters).

    String Representation:
        - Returns a string in the format of the horses "Name - Breed - Owner".
    """

    owner = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        related_name="horses"
    )
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='horse_photos/', blank=True, null=True)
    description = models.TextField(max_length=3000)

    def __str__(self):
        return f"{self.name} - {self.breed} - owner:{self.owner}"


class Job(models.Model):
    """
    Represents a job for shoeing services.

    Model Fields:
        - client: A foreign key linking to the Client model, representing the job's client.
        - date: The date the job was created.
        - next_appointment: The date of the next scheduled appointment.
        - is_paid: A boolean indicating whether the job has been paid for.
        - comments: A text field for additional details about the job.

    String Representation:
        - Returns a string in the format "Client Name - Date".
    """

    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        related_name="jobs"
    )
    date = models.DateField()
    next_appointment = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)
    
    def get_total(self):
        return sum(item.price for item in self.line_items.all())
    
    def __str__(self):
        return f"{self.client} - {self.date}"


class JobLineItem(models.Model):
    """
    Represents a line item for a job, linking a specific horse and service to the job.

    Model Fields:
        - job: A foreign key linking to the Job model, representing the job this line item belongs to.
        - horse: A foreign key linking to the Horse model, representing the horse receiving the service.
        - service: A foreign key linking to the Service model, representing the service being performed.
        - price: The price of the service for this line item, stored as a decimal with up to 8 digits and 2 decimal places.

    String Representation:
        - Returns a string in the format "Horse Name - Service Name".
    """

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="line_items"
    )
    horse = models.ForeignKey(
        Horse,
        on_delete=models.SET_NULL,
        null=True,
        related_name="line_items"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        related_name="line_items"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.horse} - {self.service}"