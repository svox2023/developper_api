from rest_framework.permissions import BasePermission

class IsClientOrMechanicForRendezVous(BasePermission):
    """
    Permissions pour les rendez-vous :
    - Les clients peuvent gérer (GET, POST, PUT, PATCH, DELETE) leurs propres rendez-vous.
    - Les mécaniciens peuvent consulter (GET) et modifier (PUT, PATCH) leurs propres rendez-vous.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Les clients peuvent accéder à toutes les méthodes (GET, POST, PUT, PATCH, DELETE)
            if hasattr(request.user, 'client') and request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                return True
            # Les mécaniciens peuvent accéder aux méthodes GET, PUT et PATCH
            if hasattr(request.user, 'mecanicien') and request.method in ['GET', 'PUT', 'PATCH']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # Si l'utilisateur est un client, il peut gérer ses propres rendez-vous
            if hasattr(request.user, 'client'):
                return obj.client.user == request.user
            # Si l'utilisateur est un mécanicien, il peut voir ou modifier ses propres rendez-vous
            if hasattr(request.user, 'mecanicien'):
                return obj.mecanicien.user == request.user
        return False
