from django.urls import path
from .views import Getstatistiques

urlpatterns = [
    path('home', Getstatistiques, name="Page_statistiques"),  # page des statistiques
]