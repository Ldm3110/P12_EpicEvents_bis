from rest_framework import permissions


class PermissionToAccessCustomer(permissions.BasePermission):
    """
    To access to a customer, user must be a member of the Sales team or be a superuser
    """
    def has_permission(self, request, view):
        if request.user.assignment.department == 'Sales' or request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        special permissions to access and perform actions to a particular customer
        """
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
