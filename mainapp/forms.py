from django.contrib.auth.models import User
from django import forms
from django.forms import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import Contact, KYC, Profile
from django_countries import countries
COUNTRY_CHOICES = tuple(countries)


class SignupForm(UserCreationForm):
    # country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=True)
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs={"type": "password", 'placeholder': ("Password")}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.TextInput(attrs={"type": "password", 'placeholder': ("Confirm Password")}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        unique_together = ('username', 'email')

        widgets = {
            'username': TextInput(attrs={'placeholder': 'Username'}),
            'first_name': TextInput(attrs={'placeholder': 'First Name', 'required': 'true'}),
            'last_name': TextInput(attrs={'placeholder': 'Last Name', 'required': 'true'}),
            'email': TextInput(attrs={'placeholder': 'Email', 'required': 'true'}),
        }



class LoginForm(forms.Form):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': ("Username")}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ("Your Password")}), label='Password')

    def clean_login(self):
        if self.username and self.password:
            raise forms.ValidationError("Password or Email Incorrect.")


# -------------------------------
#                                |
#     Profile Update
#                                |
# -------------------------------
# class ProfileForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=255)
#     last_name = forms.CharField(max_length=255)
#     email = forms.EmailField()
#
#     class Meta:
#         model = Profile
#         fields = '__all__'
#         exclude = ['user',]
#
#
# def form_validation_error(form):
#     msg = ""
#     for field in form:
#         for error in field.errors:
#             msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
#     return msg


# -------------------------------
#                                |
#     Contact
#                                |
# -------------------------------

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['phone',]

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Your Name'}),
            'email': TextInput(attrs={'placeholder': 'Enter your email'}),
            'content': TextInput(attrs={'placeholder': 'Enter your message'}),
        }


# kyc form
class KYCForm(forms.ModelForm):

    class Meta:
        model = KYC
        fields = '__all__'
        exclude = ['user', 'active',]


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
