from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Vehicule
from .serializers import VehiculeSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsClientOrMechanic


class GetVehiculeView(APIView):
    permission_classes = [IsAuthenticated, IsClientOrMechanic]

    @swagger_auto_schema(
        responses={
            200: VehiculeSerializer,
            404: "Vehicule not found."
        },
        operation_summary="Retrieve a vehicle",
        operation_description="Retrieve details of a specific vehicle by ID."
    )
    def get(self, request, pk):
        try:
            vehicule = Vehicule.objects.get(pk=pk)
            self.check_object_permissions(request, vehicule)
            serializer = VehiculeSerializer(vehicule)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehicule.DoesNotExist:
            return Response({"error": "Vehicule not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=VehiculeSerializer,
        responses={
            200: VehiculeSerializer,
            400: "Invalid data provided.",
            404: "Vehicule not found."
        },
        operation_summary="Update a vehicle",
        operation_description="Update the details of a specific vehicle by ID."
    )
    def put(self, request, pk):
        try:
            vehicule = Vehicule.objects.get(pk=pk)
            self.check_object_permissions(request, vehicule)
            serializer = VehiculeSerializer(vehicule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vehicule.DoesNotExist:
            return Response({"error": "Vehicule not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            204: "Vehicule deleted successfully.",
            404: "Vehicule not found."
        },
        operation_summary="Delete a vehicle",
        operation_description="Delete a specific vehicle by ID."
    )
    def delete(self, request, pk):
        try:
            vehicule = Vehicule.objects.get(pk=pk)
            self.check_object_permissions(request, vehicule)
            vehicule.delete()
            return Response({"message": "Vehicule deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Vehicule.DoesNotExist:
            return Response({"error": "Vehicule not found"}, status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(
        request_body=VehiculeSerializer,
        responses={
            200: VehiculeSerializer,
            400: "Invalid data provided.",
            404: "Vehicule not found."
        },
        operation_summary="Partially update a vehicle",
        operation_description="Partially update details of a specific vehicle by ID."
    )
    def patch(self, request, pk):
        try:
            vehicule = Vehicule.objects.get(pk=pk)
            self.check_object_permissions(request, vehicule)
            serializer = VehiculeSerializer(vehicule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vehicule.DoesNotExist:
            return Response({"error": "Vehicule not found"}, status=status.HTTP_404_NOT_FOUND)



class RegisterVehiculeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=VehiculeSerializer,
        responses={
            201: VehiculeSerializer,
            400: "Invalid data provided.",
            403: "Only clients can register vehicles."
        },
        operation_summary="Register a vehicle",
        operation_description="Register a new vehicle for the logged-in client."
    )
    def post(self, request):
        if not hasattr(request.user, 'client'):
            return Response({"error": "Only clients can register vehicles."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['client_id'] = request.user.client.id
        serializer = VehiculeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
