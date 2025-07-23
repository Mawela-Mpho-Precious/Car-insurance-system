from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User

class Car(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    speed = models.DecimalField(max_digits=5, decimal_places=2)  # Default to a numeric value like 0.0
    status = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)
    latitude = models.FloatField(default=0.0, null=True, blank=True)
    longitude = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return self.name
    
class FakeTransaction(models.Model):
    card_description = models.CharField(max_length=100)
    name_on_card = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)  
    cvv = models.CharField(max_length=3)
    expiry_year = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, default="pending")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.name_on_card} - {self.amount} ZAR"

class Claim(models.Model):
    CLAIM_CHOICES = [
        ('Comprehensive Claims', 'Comprehensive Claims'),
        ('Collision Claims', 'Collision Claims'),
        ('Liability Claims', 'Liability Claims'),
        ('Personal Injury Protection (PIP) Claims', 'Personal Injury Protection (PIP) Claims'),
        ('Glass And Windshield Claims', 'Glass And Windshield Claims'),
    ]
    claim_type = models.CharField(max_length=100, choices=CLAIM_CHOICES)
    full_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=15)
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.full_name    

class CarDetails(models.Model):
    car_name = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    mileage = models.CharField(max_length=50)
    year = models.DateField()

    def __str__(self):
        return f"{self.car_name} - {self.car_model} - {self.mileage}"
class UserLocation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.latitude}, {self.longitude}"
   


class CoverageSelection(models.Model):
    COVERAGE_CHOICES = [
        ('Basic', 'Basic (Liability)'),
        ('Standard', 'Standard (Liability + Collision)'),
        ('Premium', 'Premium (Full Coverage)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coverage_type = models.CharField(max_length=20, choices=COVERAGE_CHOICES)
    date_selected = models.DateTimeField(auto_now_add=True) 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One link with User model
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'  

class ClaimSubmit(models.Model):
    CLAIM_CHOICES = [
        ('Comprehensive Claims', 'Comprehensive Claims'),
        ('Collision Claims', 'Collision Claims'),
        ('Liability Claims', 'Liability Claims'),
        ('Personal Injury Protection (PIP) Claims', 'Personal Injury Protection (PIP) Claims'),
        ('Glass And Windshield Claims', 'Glass And Windshield Claims'),
    ]
    claim_type = models.CharField(max_length=100, choices=CLAIM_CHOICES)
    full_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=15)
    preferred_contact_method = models.CharField(max_length=15, choices=[('Email', 'Email'), ('Phone', 'Phone')])
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.full_name    



class ClaimAdmin(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]
    
    claim_number = models.CharField(max_length=50)
    date_submitted = models.DateField()
    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'{self.claim_number} - {self.customer_name}'
    
class Notificationpy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Admin or user receiving the notification
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)  # To mark whether the notification has been read
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
class Doc(models.Model):
     drivers_license = models.FileField(upload_to='documents/')
     Proof_Of_ID = models.FileField(upload_to='documents/')
     vehicle = models.FileField(upload_to='documents/')
     roadworthy= models.FileField(upload_to='documents/')
     income = models.FileField(upload_to='documents/')

