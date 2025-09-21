from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods for specific groups,
    only admin group can modify data.
    """
    allowed_groups = ['admin', 'receptionist', 'doctor', 'pharmacist', 'lab technician']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        # Only admin group can POST/PUT/DELETE
        return request.user.groups.filter(name='admin').exists()

class IsReceptionist(permissions.BasePermission):
    """
    Custom permission to allow receptionist and admin to modify users to access certain views.
    """
    allowed_groups = ['admin', 'receptionist', 'doctor', 'pharmacist', 'lab technician']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        # Only Receptionist group can POST/PUT/DELETE
        return request.user.groups.filter(nam__in=['admin','receptionist']).exists()

class IsDoctor(permissions.BasePermission):
    """
    Custom permission to allow doctor and admin to access certain views.
    """
    allowed_groups = ['admin', 'receptionist', 'doctor', 'pharmacist', 'lab technician']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        # Only Doctor group can POST/PUT/DELETE
        return request.user.groups.filter(name__in=['admin','doctor']).exists()

class IsPharmacist(permissions.BasePermission):
    """
    Custom permission to allow pharmacist and admin to access certain views.
    """
    allowed_groups = ['admin', 'receptionist', 'doctor', 'pharmacist', 'lab technician']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        # Only Pharmacist group can POST/PUT/DELETE
        return request.user.groups.filter(name__in=['admin','pharmacist']).exists()

class IsLabTechnician(permissions.BasePermission):
    """
    Custom permission to allow lab technician and admin to access certain views.
    """
    allowed_groups = ['admin', 'receptionist', 'doctor', 'pharmacist', 'lab technician']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        # Only Lab Technician group can POST/PUT/DELETE
        return request.user.groups.filter(name__in=['admin','lab technician']).exists()