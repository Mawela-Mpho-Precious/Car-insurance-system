from django.contrib import admin
from .models import CarDetails,ClaimSubmit,ClaimAdmin,Notificationpy,Doc,FakeTransaction
# Register your models here.
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import reverse

# Define custom admin actions
def approve_claims(modeladmin, request, queryset):
    queryset.update(status='Approved')
    # Generate notifications for all approved claims
    for claim in queryset:
        Notificationpy.objects.create(
            user=request.user,
            message=f"Claim {claim.claim_number} has been approved."
        )
    modeladmin.message_user(request, "Selected claims have been approved and notifications have been sent.")

def decline_claims(modeladmin, request, queryset):
    queryset.update(status='Declined')
    # Generate notifications for all declined claims
    for claim in queryset:
        Notificationpy.objects.create(
            user=request.user,
            message=f"Claim {claim.claim_number} has been declined."
        )
    modeladmin.message_user(request, "Selected claims have been declined and notifications have been sent.")

# Customize ClaimAdmin to include actions
@admin.register(ClaimAdmin)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_number', 'date_submitted', 'customer_name','status')
    actions = [approve_claims, decline_claims]
admin.site.register(CarDetails)
admin.site.register(ClaimSubmit)

class MyAdminSite(AdminSite):

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # You can add logic to display notifications on the main dashboard
        notifications = Notificationpy.objects.filter(user=request.user, is_read=False)
        if notifications.exists():
            # Display notification count
            notification_message = f"You have {notifications.count()} unread notifications"
            # Add a link to a custom notification page (we will define this next)
            app_list[0]['models'].append({
                'name': 'Notifications',
                'object_name': 'Notification',
                'admin_url': reverse('admin:notification_list'),  # This URL needs to be created
                'view_only': True,
            })
        return app_list

admin_site = MyAdminSite(name='myadmin')
admin.site.register(FakeTransaction)
admin.site.register(Doc)
