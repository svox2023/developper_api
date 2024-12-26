from django.urls import path
from .views import RegisterRendezVousView, GetRendezVousView

urlpatterns = [
    path('register/', RegisterRendezVousView.as_view(), name='register_rendez_vous'),
    path('<int:pk>/', GetRendezVousView.as_view(), name='get_rendez_vous'),
]
