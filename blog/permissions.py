from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Permission to only allow authenticated authors of the blog to edit it.
    """
    

    def has_object_permission(self, request, view, obj):
        
        
        return obj.author == request.user
