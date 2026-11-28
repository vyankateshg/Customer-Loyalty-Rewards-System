
from rest_framework.permissions import BasePermission


class IsAdministrator(BasePermission):

    message = "Only administrators can access this endpoint."

    def has_permission(self, request, view):

        user = request.user

        return (
            user.is_authenticated
            and user.role == "ADMINISTRATOR"
        )
