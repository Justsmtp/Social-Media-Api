from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Read: anyone; Write: only the owner of the object.
    Assumes the model has a `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, 'user_id', None) == getattr(request.user, 'id', None)
