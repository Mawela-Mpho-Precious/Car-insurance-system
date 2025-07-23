# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from binary import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
     path('home/',views.home,name='home'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    path('policy/',views.policy_coverage,name='policy'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('about/',views.aboutus,name='aboutus'),
    path('upload/',views.Upload_Doc, name = 'Upload_Doc'),
    path('payment/',views.initiate_payment,name='initiate_payment'),
    path('payment/success/',views.payment_success,name='payment_success'),
    path('create/', views.create_policy, name='create_policy'),
    path('createaccount/', views.create_account_view, name='create_account'),
    path('claim_page/', views.claim_page, name='claim_page'),
     #path('ajax/load-car-models/', views.load_car_models, name='ajax_load_car_models'),  
    path('claim_here',views.submit_claim,name='claimhere'),
    path('update-location/', views.update_location, name='update_location'),
    path('map/', views.show_map, name='show_map'),
    path('claim_success/', views.claim_success, name='claim_success'),
    path('roadside-assistance/', views.roadside_assistance, name='roadside_assistance'),
    path('chat/',views.chat,name='chat'),
    path('submit/', views.submit_claim, name='submit_claim'),
    path('admin/approve/<int:claim_id>/', views.approve_claim, name='approve_claim'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
