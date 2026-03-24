from django import forms

from .models import Client, Job, JobLineItem, Service, Horse


# Model Forms
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'photo': 'Client Image',
            'business_name': 'Business',
            'phone_number': 'Phone Number',
            'email': 'Email'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'first-name',
                'name': 'first-name',
                'class': 'first-name'
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'last-name',
                'name': 'last-name',
                'class': 'last-name',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'id': 'client-image',
                'name': 'client-image',
                'class': 'client-image'
            }),
            'business_name': forms.TextInput(attrs={
                'id': 'business',
                'name': 'business',
                'class': 'business',
                'placeholder': 'Business name',
            }),
            'phone_number': forms.TextInput(attrs={
                'id': 'phone-number',
                'name': 'phone-number',
                'class': 'phone-number',
                'type': 'tel',
                'placeholder': '(xxx) xxx-xxxx',
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'name': 'email',
                'class': 'email',
                'placeholder': 'Example@email.com'
            })
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'date',
            'client',
            'is_paid',
            'next_appointment',
            'comments'
        ]
        labels = {
            'date': 'Date',
            'client': 'Client',
            'is_paid': 'Paid?',
            'next_appointment': 'Next Appt',
            'comments': 'Comments'
        }
        widgets = {
            'date': forms.DateInput(attrs={
                'id': 'job-date',
                'name': 'job-date',
                'class': 'job-date',
                'type': 'date'
            }),
            'client' : forms.Select(attrs={
                'id': 'client',
                'name': 'client',
                'class': 'client',
            }),
            'is_paid': forms.CheckboxInput(attrs={
                'id': 'is-paid',
                'name': 'is-paid',
                'class': 'is-paid'
            }),
            'next_appointment': forms.DateInput(attrs={
                'id': 'next-appt',
                'name': 'next-appt',
                'class': 'next-appt',
                'type': 'date'
            }),
            'comments': forms.Textarea(attrs={
                'id': 'job-comments',
                'name': 'job-comments',
                'placeholder': 'Job comments go here...',
            })
        }
    

class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        fields = [
            'name',
            'breed',
            'photo',
            'description'
        ]
        labels = {
            'name': 'Name',
            'breed': 'Breed',
            'photo': 'Horse Image',
            'description': 'Description'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'horse-name',
                'name': 'horse-name',
                'class': 'horse-name'
            }),
            'breed': forms.TextInput(attrs={
                'id': 'breed',
                'name': 'breed',
                'class': 'breed',
                'placeholder': 'Thoroughbred'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'id': 'horse-image',
                'name': 'horse-image',
                'class': 'horse-image'
            }),
            'description': forms.Textarea(attrs={
                'id': 'horse-description',
                'name': 'horse-description',
                'placeholder': 'Give a description of the horse...',
            })
        }