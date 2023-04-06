# cats/permissions.py

from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
            )

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
