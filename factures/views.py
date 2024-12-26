from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Facture, Vehicule
from .serializers import FactureSerializer
from .permissions import IsClientOrMechanicForFacture
from rest_framework.permissions import IsAuthenticated


class RegisterFactureView(APIView):
    permission_classes = [IsAuthenticated, IsClientOrMechanicForFacture]

    @swagger_auto_schema(
        request_body=FactureSerializer,
        responses={
            201: FactureSerializer,
            400: "Invalid data provided.",
            403: "Only mechanics can create invoices."
        },
        operation_summary="Create a new invoice",
        operation_description="Allows mechanics to create an invoice."
    )
    def post(self, request):
        self.check_permissions(request)  # Vérifie les permissions au niveau de la requête

        if hasattr(request.user, 'mecanicien'):
            data = request.data.copy()
            data['mecanicien_id'] = request.user.mecanicien.id  # Associe automatiquement le mécanicien connecté

            # Vérifier si le véhicule existe et récupérer son client
            try:
                vehicule = Vehicule.objects.get(pk=data['vehicule_id'])
                data['client'] = vehicule.client.id  # Associer automatiquement le client du véhicule
            except Vehicule.DoesNotExist:
                return Response({"error": "Invalid vehicle ID provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Sérialiser et sauvegarder la facture
            serializer = FactureSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Only mechanics can create invoices."}, status=status.HTTP_403_FORBIDDEN)

    



class GetFactureView(APIView):
    permission_classes = [IsAuthenticated, IsClientOrMechanicForFacture]

    @swagger_auto_schema(
        responses={
            200: FactureSerializer,
            404: "Facture not found."
        },
        operation_summary="Retrieve a specific invoice",
        operation_description="Allows authorized users to retrieve a specific invoice by ID."
    )
    def get(self, request, pk):
        try:
            facture = Facture.objects.get(pk=pk)
            self.check_object_permissions(request, facture)
            serializer = FactureSerializer(facture)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Facture.DoesNotExist:
            return Response({"error": "Facture not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=FactureSerializer,
        responses={
            200: FactureSerializer,
            400: "Invalid data provided.",
            404: "Facture not found."
        },
        operation_summary="Update an entire invoice",
        operation_description="Allows authorized users to fully update an existing invoice."
    )
    def put(self, request, pk):
        try:
            facture = Facture.objects.get(pk=pk)
            self.check_object_permissions(request, facture)
            serializer = FactureSerializer(facture, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Facture.DoesNotExist:
            return Response({"error": "Facture not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=FactureSerializer,
        responses={
            200: FactureSerializer,
            400: "Invalid data provided.",
            404: "Facture not found."
        },
        operation_summary="Partially update an invoice",
        operation_description="Allows authorized users to partially update an existing invoice."
    )
    def patch(self, request, pk):
        try:
            facture = Facture.objects.get(pk=pk)
            self.check_object_permissions(request, facture)
            serializer = FactureSerializer(facture, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Facture.DoesNotExist:
            return Response({"error": "Facture not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            204: "Facture deleted successfully.",
            404: "Facture not found."
        },
        operation_summary="Delete an invoice",
        operation_description="Allows authorized users to delete an invoice."
    )
    def delete(self, request, pk):
        try:
            facture = Facture.objects.get(pk=pk)
            self.check_object_permissions(request, facture)
            facture.delete()
            return Response({"message": "Facture deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Facture.DoesNotExist:
            return Response({"error": "Facture not found"}, status=status.HTTP_404_NOT_FOUND)
