from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User, Client, Job, LineItem, Horse


# User Auth Forms
class RegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""

    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'name': 'username',
        'class': 'username',
        'placeholder': 'Username',
        'autocomplete': 'off'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'name': 'email',
        'class': 'email',
        'placeholder': 'Email@example.com',
        'autocomplete': 'on'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'name': 'password',
        'class': 'password',
        'placeholder': 'Password',
        'autocomplete': 'new-password'
    }))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'confirmation',
        'name': 'confirmation',
        'class': 'confirmation',
        'placeholder': 'Confirm password',
        'autocomplete': 'off'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
        
        return username

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
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""

    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'name': 'username',
        'class': 'username',
        'placeholder': 'Username',
        'autocomplete': 'on'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'name': 'password',
        'class': 'password',
        'placeholder': 'Password',
        'autocomplete': 'current-password'
    }))


# Model Forms
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'photo',
            'business_name',
            'phone_number',
            'email'
        ]
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'photo': 'Photo',
            'business_name': 'Business',
            'phone_number': 'Phone Number',
            'email': 'Email'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'first-name',
                'class': 'first-name',
                'placeholder': 'First Name',
                'autocomplete': 'new-password'
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'last-name',
                'class': 'last-name',
                'placeholder': 'Last Name',
                'autocomplete': 'new-password'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'id': 'client-image',
                'class': 'client-image'
            }),
            'business_name': forms.TextInput(attrs={
                'id': 'business',
                'class': 'business',
                'placeholder': 'Business name'
            }),
            'phone_number': forms.TextInput(attrs={
                'id': 'phone-number',
                'class': 'phone-number',
                'type': 'tel',
                'placeholder': '(xxx) xxx-xxxx',
                'autocomplete': 'new-password'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'email',
                'placeholder': 'Example@email.com',
                'autocomplete': 'new-password'
            })
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'client',
            'is_paid',
            'appointment',
            'comments'
        ]
        labels = {
            'client': 'Client',
            'is_paid': 'Paid?',
            'appointment': 'Appt date & time',
            'comments': ''
        }
        widgets = {
            'client' : forms.Select(attrs={
                'id': 'client',
                'class': 'client',
            }),
            'is_paid': forms.CheckboxInput(attrs={
                'id': 'is-paid',
                'class': 'is-paid'
            }),
            'appointment': forms.DateTimeInput(attrs={
                'id': 'next-appt',
                'class': 'next-appt',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
            'comments': forms.Textarea(attrs={
                'id': 'job-comments',
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
                'class': 'horse-name'
            }),
            'breed': forms.TextInput(attrs={
                'id': 'breed',
                'class': 'breed',
                'placeholder': 'Thoroughbred'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'id': 'horse-image',
                'class': 'horse-image'
            }),
            'description': forms.Textarea(attrs={
                'id': 'horse-description',
                'placeholder': 'Give a description of the horse...',
            })
        }


class LineItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)

        if client:
            self.fields['horse'].queryset = Horse.objects.filter(owner=client)

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
                'class': 'horse'
            }),
            'service' : forms.Select(attrs={
                'id': 'service',
                'class': 'service'
            }),
            'price' : forms.NumberInput(attrs={
                'id': 'price',
                'class': 'price'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        horse = cleaned_data.get('horse')
        job = self.instance.job if self.instance else None
        
        if horse and job and horse.owner != job.client:
            raise forms.ValidationError(
                'This horse does not belong to the client on this job.'
            )
        
        return cleaned_data