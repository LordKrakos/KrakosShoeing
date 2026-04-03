from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User, Client, Job, LineItem, Service, Horse


# User Auth Forms
class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'name': 'username',
        'class': 'username',
        'placeholder': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'name': 'email',
        'class': 'email',
        'placeholder': 'Email@example.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'name': 'password',
        'class': 'password',
        'placeholder': 'password'
    }))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'confirmation',
        'name': 'confirmation',
        'class': 'confirmation',
        'placeholder': 'Confirm password'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirmation = cleaned_data.get('confirmation')

        if password != confirmation:
            raise forms.ValidationError('Password and confirmation must match.')
        
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'name': 'username',
        'class': 'username',
        'placeholder': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'name': 'password',
        'class': 'password',
        'placeholder': 'password'
    }))


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
                'class': 'last-name'
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
                'placeholder': 'Business name'
            }),
            'phone_number': forms.TextInput(attrs={
                'id': 'phone-number',
                'name': 'phone-number',
                'class': 'phone-number',
                'type': 'tel',
                'placeholder': '(xxx) xxx-xxxx'
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


class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = [
            'horse',
            'service',
            'price'
        ]
        labels = {
            'horse': 'Horse',
            'service': 'Service',
            'price': 'Price'
        }
        widgets = {
            'horse' : forms.Select(attrs={
                'id': 'horse',
                'name': 'horse',
                'class': 'horse'
            }),
            'service' : forms.Select(attrs={
                'id': 'service',
                'name': 'service',
                'class': 'service'
            }),
            'price' : forms.NumberInput(attrs={
                'id': 'price',
                'name': 'price',
                'class': 'price'
            }),
        }