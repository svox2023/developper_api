from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Client, Mecanicien
from .serializers import ClientSerializer, MecanicienSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsMechanic, IsClient
from rest_framework_simplejwt.tokens import RefreshToken


class GetClientView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: ClientSerializer,
            403: "Access denied.",
            404: "Client not found."
        },
        operation_summary="Retrieve a client",
        operation_description="Retrieve a client's information. A client can access their own profile, while a mechanic can only access clients assigned to them."
    )
    def get(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)

            # Si l'utilisateur est un client, il peut accéder uniquement à son propre profil
            if hasattr(request.user, 'client') and request.user.client != client:
                return Response(
                    {"error": "Access denied: You can only view your own profile."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Si l'utilisateur est un mécanicien, il peut accéder uniquement aux clients qui lui sont assignés
            if hasattr(request.user, 'mecanicien') and client.mecanicien != request.user.mecanicien:
                return Response(
                    {"error": "Access denied: This client is not assigned to you."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=ClientSerializer,
        responses={
            200: ClientSerializer,
            400: "Invalid data provided.",
            403: "Access denied.",
            404: "Client not found."
        },
        operation_summary="Update a client",
        operation_description="Update a client's information. Only the client can update their own profile."
    )
    def put(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)

            # Vérifie si l'utilisateur est un client et accède à son propre profil
            if not (hasattr(request.user, 'client') and request.user.client == client):
                return Response(
                    {"error": "Access denied: You can only update your own profile."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = ClientSerializer(client, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=ClientSerializer,
        responses={
            200: ClientSerializer,
            400: "Invalid data provided.",
            403: "Access denied.",
            404: "Client not found."
        },
        operation_summary="Partially update a client",
        operation_description="Partially update a client's information. Only the client can update their own profile."
    )
    def patch(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)

            # Vérifie si l'utilisateur est un client et accède à son propre profil
            if not (hasattr(request.user, 'client') and request.user.client == client):
                return Response(
                    {"error": "Access denied: You can only update your own profile."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = ClientSerializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            204: "Client deleted successfully.",
            403: "Access denied.",
            404: "Client not found."
        },
        operation_summary="Delete a client",
        operation_description="Delete a client's information. Only the client can delete their own profile."
    )
    def delete(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)

            # Vérifie si l'utilisateur est un client et accède à son propre profil
            if not (hasattr(request.user, 'client') and request.user.client == client):
                return Response(
                    {"error": "Access denied: You can only delete your own profile."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            client.delete()
            client.user.delete()  # Supprime également l'entrée dans auth_user

            return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


class RegisterClientView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(

        request_body=ClientSerializer,
        responses={
            201: "Client registered successfully.",
            400: "Invalid data provided."
        },
       
        operation_summary="Register a new client",
        operation_description="Create a new client and generate JWT tokens."
    )
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            refresh = RefreshToken.for_user(client.user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterMecanicienView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=MecanicienSerializer,
        responses={
            201: "Mechanic registered successfully.",
            400: "Invalid data provided."
        },
        operation_summary="Register a new mechanic",
        operation_description="Create a new mechanic and generate JWT tokens."
    )
    def post(self, request):
        serializer = MecanicienSerializer(data=request.data)
        if serializer.is_valid():
            mecanicien = serializer.save()
            refresh = RefreshToken.for_user(mecanicien.user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetMecanicienView(APIView):
    permission_classes = [IsAuthenticated, IsMechanic]

    @swagger_auto_schema(
        responses={
            200: MecanicienSerializer,
            404: "Mechanic not found."
        },
        operation_summary="Retrieve a mechanic",
        operation_description="Retrieve a mechanic's information by ID."
    )
    def get(self, request, pk):
        try:
            mecanicien = Mecanicien.objects.get(pk=pk)
            serializer = MecanicienSerializer(mecanicien)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Mecanicien.DoesNotExist:
            return Response({"error": "Mechanic not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=MecanicienSerializer,
        responses={
            200: MecanicienSerializer,
            400: "Invalid data provided.",
            404: "Mechanic not found."
        },
        operation_summary="Update a mechanic",
        operation_description="Update a mechanic's information by ID."
    )
    def put(self, request, pk):
        try:
            mecanicien = Mecanicien.objects.get(pk=pk)
            serializer = MecanicienSerializer(mecanicien, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Mecanicien.DoesNotExist:
            return Response({"error": "Mechanic not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=MecanicienSerializer,
        responses={
            200: MecanicienSerializer,
            400: "Invalid data provided.",
            404: "Mechanic not found."
        },
        operation_summary="Partially update a mechanic",
        operation_description="Partially update a mechanic's information by ID."
    )
    def patch(self, request, pk):
        try:
            mecanicien = Mecanicien.objects.get(pk=pk)
            serializer = MecanicienSerializer(mecanicien, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Mecanicien.DoesNotExist:
            return Response({"error": "Mechanic not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            204: "Mechanic deleted successfully.",
            404: "Mechanic not found."
        },
        operation_summary="Delete a mechanic",
        operation_description="Delete a mechanic by ID."
    )
    def delete(self, request, pk):
        try:
            mecanicien = Mecanicien.objects.get(pk=pk)
            mecanicien.delete()
            mecanicien.user.delete()
            return Response({"message": "Mechanic deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Mecanicien.DoesNotExist:
            return Response({"error": "Mechanic not found"}, status=status.HTTP_404_NOT_FOUND)
