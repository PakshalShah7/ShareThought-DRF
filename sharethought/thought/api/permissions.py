from rest_framework.permissions import BasePermission


class ThoughtPermissions(BasePermission):
    def has_permission(self, request, view):
        if (
            view.action in ["create", "update", "destroy"]
            and request.user.groups.filter(name="authors").exists()
        ):
            return True
        elif view.action in ["list", "retrieve"]:
            return True
        else:
            return False
