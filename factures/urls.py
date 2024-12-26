from django.urls import path
from .views import RegisterFactureView, GetFactureView

urlpatterns = [
    path('register/', RegisterFactureView.as_view(), name='register-facture'),  # POST : ajouter une facture
    path('<int:pk>/', GetFactureView.as_view(), name='get-update-delete-facture'),  # GET, PUT, PATCH, DELETE
]
