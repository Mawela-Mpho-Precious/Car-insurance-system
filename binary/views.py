from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from .forms import CustomUserCreationForm, CustomLoginForm,CoverageForm
from .models import FakeTransaction,CarDetails,CoverageSelection,Claim,UserProfile
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import Car
import uuid
from .forms  import ClaimForm,CarDetailsForm,ClaimsForm
from .models import UserLocation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Notificationpy



def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  
    else:
        form = CustomLoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def policy_coverage(request):
    if request.method == 'POST':
        form = CoverageForm(request.POST)
        if form.is_valid():
            # Save the selection in the database
            CoverageSelection.objects.create(
                user=request.user, 
                coverage_type=form.cleaned_data['coverage_type']
            )
            return redirect('initiate_payment')  # Redirect to a success page after submission
    else:
        form = CoverageForm()

    return render(request,'policy/policy_amount.html')

def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    context = {
        'car': car,
    }
    return render(request, 'tracking/car_detail.html', context)

def aboutus(request):
    return render(request,'aboutus.html')

def initiate_payment(request):
    if request.method == 'POST':
        card_description = request.POST.get('card_description')
        name_on_card = request.POST.get('name_on_card')
        card_number = request.POST.get('card_number')
        cvv = request.POST.get('cvv')
        expiry_year = request.POST.get('expiry_year')
        amount = request.POST.get('amount')

       
        transaction_id = str(uuid.uuid4())

        transaction = FakeTransaction.objects.create(
            card_description=card_description,
            name_on_card=name_on_card,
            card_number=card_number[-4:],  
            cvv=cvv,
            expiry_year=expiry_year,
            amount=amount,
            transaction_id=transaction_id,
            status="successful"  
        )

        # Redirect to the success page
        return redirect('payment_success')

    return render(request, 'policy/initiate_payment.html')

def create_policy(request):
    if request.method == 'POST':
        form = CarDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('policy')  # Redirect to the policy page after saving the form
        else:
            error = 'Please fill out all fields.'
    else:
        form = CarDetailsForm()
        error = ''  # No error message if it's a GET request

    # Merge form and error into one dictionary
    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'policy/create_policy.html', context)
    

def claim_page(request):
    return render(request, 'claims/claims.html')
def claim_success(request):
    return render(request, 'claims/claims_success.html')
def payment_success(request):
   
    context = {
        'transaction_id': '001',
        'amount': '100.00'  
    }
    return render(request, 'policy/payment_success.html', context)






def create_account_view(request):
    if request.method == 'POST':
        form = CarDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('policy')  # Redirect to policy page after submission
    else:
        form = CarDetailsForm()
    
    return render(request, 'policy/create_account.html', {'form': form})

@csrf_exempt
def update_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        # Save location data
        UserLocation.objects.create(user=user, latitude=latitude, longitude=longitude)
        return JsonResponse({"status": "Location updated!"})
    return JsonResponse({"status": "Invalid request method"}, status=400)

def show_map(request):
    latitude = 51.505  # Default value or get from your model
    longitude = -0.09  # Default value or get from your model
    context = {
        'latitude': latitude,
        'longitude': longitude,
    }
    return render(request, 'tracking/car_tracker.html', context)

def roadside_assistance(request):
    return render(request, 'roadside_assistance.html')

def chat(request):
    return render(request, 'chat.html')

@login_required
def profile_view(request):
    user_profile = request.user.userprofile  # Access the user's profile
    context = {
        'profile': user_profile
    }
    return render(request, 'profile.html', context)

def submit_claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('claim_success')
    else:
        form = ClaimForm()
    return render(request, 'claims/claim_form.html', {'form': form})



def admin_claims(request):
    claims = Claim.objects.all()
    return render(request, 'claims/admin_claims.html', {'claims': claims})

def approve_claim(request, claim_id):
    claim = Claim.objects.get(id=claim_id)
    claim.approved = True
    claim.save()
    return redirect('admin_claims')

from .forms import DocumentUploadForm  # Ensure the form is imported

def Upload_Doc(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
           

            # Redirect after successful upload
            return redirect('initiate_payment')  # Replace with the correct success page
    else:
        form = DocumentUploadForm()

    return render(request, 'policy/Upload_Doc.html', {'form': form})


class NotificationListView(ListView):
    model = Notificationpy
    template_name = 'admin/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        # Filter notifications for the logged-in admin user and mark as read after viewing
        queryset = Notificationpy.objects.filter(user=self.request.user, is_read=False)
        queryset.update(is_read=True)
        return queryset
def approve_claim(request, claim_id):
    # Code to approve the claim...
    messages.success(request, "Claim approved successfully!")
    return redirect('home')

def decline_claim(request, claim_id):
    # Code to decline the claim...
    messages.error(request, "Claim declined.")
    return redirect('home')
   

