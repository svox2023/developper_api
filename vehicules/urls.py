from django.urls import path
from .views import GetVehiculeView, RegisterVehiculeView

urlpatterns = [
    path('register/vehicule/', RegisterVehiculeView.as_view(), name='register-vehicule'),  # POST pour ajouter un véhicule
    path('vehicule/<int:pk>/', GetVehiculeView.as_view(), name='get-update-delete-vehicule'),  # GET, PUT, PATCH, DELETE
]