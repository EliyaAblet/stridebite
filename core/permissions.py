# core/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAppUser(BasePermission):
    """
    Allow access only to authenticated users who belong to the 'App User' group
    or are superusers.

    We’ll use this on the API viewsets so only real application users can
    create/update/delete data.
    """

    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated first
        if not user or not user.is_authenticated:
            return False

        # Superusers always allowed
        if user.is_superuser:
            return True

        # Check if user is in the "App User" group
        return user.groups.filter(name="App User").exists()
