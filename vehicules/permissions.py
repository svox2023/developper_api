from rest_framework.permissions import BasePermission

class IsClientOrMechanic(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est un client et a enregistré ce véhicule
        if hasattr(request.user, 'client') and obj.client_id == request.user.client.id:
            return True
        
        # Vérifie si l'utilisateur est un mécanicien, utilise une méthode GET,
        # et est le mécanicien assigné au client propriétaire de ce véhicule
        if (
            hasattr(request.user, 'mecanicien') and 
            request.method == 'GET' and 
            obj.client.mecanicien_id == request.user.mecanicien.id
        ):
            return True
        
        return False
