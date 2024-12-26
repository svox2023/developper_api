from django.urls import path
from .views import RegisterClientView, RegisterMecanicienView, GetClientView, GetMecanicienView

urlpatterns = [
    path('register/client/', RegisterClientView.as_view(), name='register_client'),  # POST pour enregistrer un client
    path('register/mecanicien/', RegisterMecanicienView.as_view(), name='register_mecanicien'),  # POST pour enregistrer un mécanicien
    path('client/<int:pk>/', GetClientView.as_view(), name='manage_client'),  # GET, PUT, PATCH, DELETE pour un client
    path('mecanicien/<int:pk>/', GetMecanicienView.as_view(), name='manage_mecanicien'),  # GET , PUT , PATCH pour un mécanicien
]
