from rest_framework import permissions

class PaymentDetailsPermission(permissions.BasePermission):

    # only allow access if the video revision belongs to a users video
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False