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
