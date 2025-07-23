
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import FakeTransaction
from .models import Claim
from .models import CarDetails
from.models import ClaimSubmit


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Please enter your name')
    email = forms.EmailField(label='Please enter your email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Please enter your name:', max_length=254)
    password = forms.CharField(label='Please enter your password', widget=forms.PasswordInput)

class PaymentForm(forms.ModelForm):
    class Meta:
        model=FakeTransaction
        fields=['card_description','name_on_card','card_number','cvv','expiry_year']

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_type', 'full_name', 'policy_number', 'email_address', 'phone_number', 'document']
        widgets = {
            'claim_type': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CarDetailsForm(forms.ModelForm):
    class Meta:
        model = CarDetails
        fields = ['car_name', 'car_model', 'mileage', 'year']

COVERAGE_CHOICES = [
    ('Basic', 'Basic (Liability)'),
    ('Standard', 'Standard (Liability + Collision)'),
    ('Premium', 'Premium (Full Coverage)'),
]
class CoverageForm(forms.Form):
    coverage_type = forms.ChoiceField(choices=COVERAGE_CHOICES)

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_type', 'full_name', 'policy_number', 'email_address', 'phone_number',  'document']
        widgets = {
            'claim_type': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class ClaimsForm(forms.ModelForm):
     model = Claim
     fields = ['claim_type', 'full_name', 'policy_number', 'email_address', 'phone_number', 'document']

class DocumentUploadForm(forms.Form):
    driver_license = forms.FileField(label="Driver's License", required=True)
    identity_document = forms.FileField(label="Proof of Identity (ID/Passport)", required=True)
    vehicle_registration = forms.FileField(label="Vehicle Registration Papers", required=True)
    vehicle_ownership = forms.FileField(label="Proof of Vehicle Ownership", required=True)
    roadworthy_certificate = forms.FileField(label="Roadworthy Certificate", required=False)
    proof_of_income = forms.FileField(label="Proof of Income (Payslip/Bank Statement)", required=False)
     



   

