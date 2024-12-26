from rest_framework.permissions import BasePermission

class IsClientOrMechanicForFacture(BasePermission):
    """
    Permission customisée pour les factures :
    - Les clients peuvent consulter (GET) uniquement les factures liées à leurs véhicules.
    - Les mécaniciens peuvent gérer (POST, PUT, PATCH, DELETE) uniquement les factures qui leur sont associées.
    """

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Si l'utilisateur est un client
            if hasattr(request.user, 'client'):
                # Le client peut uniquement voir (GET) les factures de ses propres véhicules
                if request.method == 'GET':
                    return obj.vehicule.client.user == request.user

            # Si l'utilisateur est un mécanicien
            elif hasattr(request.user, 'mecanicien'):
                # Le mécanicien peut gérer (POST, PUT, PATCH, DELETE) uniquement ses propres factures
                return obj.mecanicien.user == request.user

        # Refuse l'accès si aucune condition n'est remplie
        return False
