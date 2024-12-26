from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Client, Mecanicien


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle User de Django.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False, 'help_text': "Mot de passe de l'utilisateur (haché automatiquement)"},
        }

    def create(self, validated_data):
        """
        Création d'un utilisateur avec hachage automatique du mot de passe.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    def update(self, instance, validated_data):
        """
        Mise à jour des informations utilisateur.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Client.
    """
    user = UserSerializer()  # Création d'un utilisateur pour le client
    mecanicien = serializers.StringRelatedField(read_only=True)  # Affichage du mécanicien en lecture seule
    mecanicien_id = serializers.PrimaryKeyRelatedField(
        queryset=Mecanicien.objects.all(),
        write_only=True,
        source='mecanicien',
        help_text="ID du mécanicien associé au client",
        required=True  # L'ID du mécanicien est requis
    )

    class Meta:
        model = Client
        fields = ['user', 'birth_date', 'mecanicien', 'mecanicien_id']

    def create(self, validated_data):
        """
        Création d'un client avec un utilisateur et un mécanicien associés.
        """
        # Extraire les données utilisateur et l'ID du mécanicien
        user_data = validated_data.pop('user')
        mecanicien = validated_data.pop('mecanicien')

        # Créer l'utilisateur associé au client
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )

        # Créer le client avec l'utilisateur et le mécanicien
        client = Client.objects.create(user=user, mecanicien=mecanicien, **validated_data)
        return client

    def update(self, instance, validated_data):
        """
        Mise à jour des informations d'un client.
        """
        user_data = validated_data.pop('user', None)
        mecanicien = validated_data.pop('mecanicien', None)

        # Mettre à jour les informations utilisateur
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        # Mettre à jour les autres champs du client
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if mecanicien:
            instance.mecanicien = mecanicien
        instance.save()
        return instance



class MecanicienSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Mecanicien.
    """
    user = UserSerializer()  

    class Meta:
        model = Mecanicien
        fields = ['user', 'birth_date', 'specialite', 'disponibilite']

    def create(self, validated_data):
        """
        Création d'un mécanicien.
        """
        user_data = validated_data.pop('user', None)
        if not user_data:
            raise serializers.ValidationError({"user": "Les informations utilisateur sont obligatoires."})

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)  # Crée un utilisateur
        return Mecanicien.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        """
        Mise à jour des informations d'un mécanicien.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


