from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import RendezVous
from .serializers import RendezVousSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsClientOrMechanicForRendezVous


class RegisterRendezVousView(APIView):
    permission_classes = [IsAuthenticated, IsClientOrMechanicForRendezVous]

    @swagger_auto_schema(
        request_body=RendezVousSerializer,
        responses={
            201: RendezVousSerializer,
            400: "Invalid data provided.",
        },
        operation_summary="Create an appointment",
        operation_description="Allows clients to create an appointment."
    )
    def post(self, request):
        # La permission `IsClientOrMechanicForRendezVous` garantit que seuls les clients peuvent créer des rendez-vous
        data = request.data.copy()
        data['client_id'] = request.user.client.id  # Associe automatiquement le client connecté

        serializer = RendezVousSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRendezVousView(APIView):
    permission_classes = [IsAuthenticated, IsClientOrMechanicForRendezVous]

    @swagger_auto_schema(
        responses={
            200: RendezVousSerializer,
            404: "Rendez-vous not found."
        },
        operation_summary="Retrieve an appointment",
        operation_description="Allows authorized users to retrieve an appointment by ID."
    )
    def get(self, request, pk):
        try:
            rendez_vous = RendezVous.objects.get(pk=pk)
            self.check_object_permissions(request, rendez_vous)
            serializer = RendezVousSerializer(rendez_vous)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RendezVous.DoesNotExist:
            return Response({"error": "Rendez-vous not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=RendezVousSerializer,
        responses={
            200: RendezVousSerializer,
            400: "Invalid data provided.",
            404: "Rendez-vous not found."
        },
        operation_summary="Update an appointment",
        operation_description="Allows authorized users to update an appointment."
    )
    def put(self, request, pk):
        try:
            rendez_vous = RendezVous.objects.get(pk=pk)
            self.check_object_permissions(request, rendez_vous)

            serializer = RendezVousSerializer(rendez_vous, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RendezVous.DoesNotExist:
            return Response({"error": "Rendez-vous not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=RendezVousSerializer,
        responses={
            200: RendezVousSerializer,
            400: "Invalid data provided.",
            404: "Rendez-vous not found."
        },
        operation_summary="Partially update an appointment",
        operation_description="Allows authorized users to partially update an appointment."
    )
    def patch(self, request, pk):
        try:
            rendez_vous = RendezVous.objects.get(pk=pk)
            self.check_object_permissions(request, rendez_vous)

            serializer = RendezVousSerializer(rendez_vous, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RendezVous.DoesNotExist:
            return Response({"error": "Rendez-vous not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            204: "Rendez-vous deleted successfully.",
            404: "Rendez-vous not found."
        },
        operation_summary="Delete an appointment",
        operation_description="Allows authorized users to delete an appointment."
    )
    def delete(self, request, pk):
        try:
            rendez_vous = RendezVous.objects.get(pk=pk)
            self.check_object_permissions(request, rendez_vous)

            rendez_vous.delete()
            return Response({"message": "Rendez-vous deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except RendezVous.DoesNotExist:
            return Response({"error": "Rendez-vous not found"}, status=status.HTTP_404_NOT_FOUND)
