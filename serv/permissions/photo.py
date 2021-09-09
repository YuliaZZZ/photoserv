from rest_framework import permissions


class HasPermissionsForPhoto(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        """Has permission."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        """Has object permission."""
        if request.user.is_superuser:
            return True
        return obj.owner == request.user
