from rest_framework.permissions import BasePermission
from Vendor.models import Vendor

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return True
        return False
    

class CustomProductPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Vendor.objects.filter(user=request.user).exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if Vendor.objects.filter(user=request.user).exists():
                if obj.vendor.user == request.user:
                    return True
        return False