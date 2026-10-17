from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Register


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
        max_length=150
    )

    last_name = forms.CharField(
        required=True,
        max_length=150
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = Register

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',

            # Contact information
            'whatsapp_number',
            'other_number',
            'address',

            # Blood information
            'blood_group',
            'last_donation_date',

            # Donor information
            'is_donor',
            'age',
            'weight',
            'university_batch',
        ]

        widgets = {

            'last_donation_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter your address'
                }
            ),

            'weight': forms.NumberInput(
                attrs={
                    'step': '0.1',
                    'min': '30',
                    'placeholder': 'Enter your weight in kg'
                }
            ),

            'age': forms.NumberInput(
                attrs={
                    'min': '18',
                    'max': '100',
                    'placeholder': 'Enter your age'
                }
            ),

            'university_batch': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Fall23 or Spring23'
                }
            ),
        }