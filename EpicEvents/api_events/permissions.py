from rest_framework import permissions


class EventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        1. If request method is a POST -> look if the user is member of team Support
        - if it's true -> permission denied
        - if it's false -> permission granted

        2. if it's an other request method -> look if the user is member of team Sales
        - if it's true -> permission denied
        - if it's false -> permission granted
        """
        if request.method == 'POST':
            if request.user.assignment.department == 'Support':
                return False
            return True
        elif request.user.assignment.department == 'Sales':
            return False

        return True

    def has_object_permission(self, request, view, obj):
        """
        Check if the User is the support contact of this event
        """
        if obj[0].support_contact == request.user:
            return True

        return False


class CustomerInEventPermissions(permissions.BasePermission):
    """
    Specifics permissions to allow the 'Support' User to access at a customer of an event
    """

    def has_object_permission(self, request, view, obj):
        if obj[0].support_contact == request.user:
            return True

        return False
