from django.urls import path
from binary import consumers

websocket_urlpatterns = [
    path('ws/car/<int:car_id>/', consumers.CarConsumer.as_asgi()),
]