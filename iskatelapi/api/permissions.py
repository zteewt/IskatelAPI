from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    ONLY THE ADMINISTRATOR OR THE OWNER 
    OF THE OBJECT CAN DELETE AN OBJECT
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user and request.user.is_staff:
            return True
        
        return obj.user == request.user