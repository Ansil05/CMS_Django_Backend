from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Role, Specialization, Staff, Doctor
from .serializers import (
    RoleSerializer, SpecializationSerializer,
    StaffSerializer, DoctorSerializer
)

# ---- Optional custom permission ----
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow only Admin users to create/update/delete.
    Others can only view (GET).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff  # Django admin user


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrReadOnly]


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdminOrReadOnly]


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdminOrReadOnly]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related("Staff", "Specialization")
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Allow filtering by specialization or availability from query params
        Example: /api/doctors/?specialization=2&availability=Available
        """
        queryset = super().get_queryset()
        specialization = self.request.query_params.get("specialization")
        availability = self.request.query_params.get("availability")

        if specialization:
            queryset = queryset.filter(Specialization__id=specialization)
        if availability:
            queryset = queryset.filter(availability=availability)

        return queryset
