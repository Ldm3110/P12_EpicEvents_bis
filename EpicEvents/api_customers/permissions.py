from rest_framework import permissions


class PermissionToAccessCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.assignment.department == 'Sales' or request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in {'GET', 'POST'}:
            if obj[0].sales_contact == request.user:
                return True
        elif request.method == 'PATCH':
            if obj.sales_contact == request.user:
                return True
        elif request.method == "DELETE":
            if request.user.is_superuser:
                return True

        return False
