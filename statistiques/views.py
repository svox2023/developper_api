from django.shortcuts import render
from django.db.models import Count, Sum, Q
from utilisateurs.models import Client, Mecanicien
from vehicules.models import Vehicule
from rendez_vous.models import RendezVous
from factures.models import Facture

def Getstatistiques(request):
    statistiques = {
        'total_clients': Client.objects.count(),
        'total_mechanics': Mecanicien.objects.count(),
        'total_rendez_vous': RendezVous.objects.count(),
        'rendez_vous_status': {
            'en_attente': RendezVous.objects.filter(status='en_attente').count(),
            'confirme': RendezVous.objects.filter(status='confirme').count(),
            'annule': RendezVous.objects.filter(status='annule').count(),
            'termine': RendezVous.objects.filter(status='termine').count(),
        },
        'total_paiements': Facture.objects.aggregate(total=Sum('montant'))['total'],
        'total_vehicules': Vehicule.objects.count(),
    }
    return render(request, "statistiques/Getstatistiques.html", {"statistiques": statistiques})


