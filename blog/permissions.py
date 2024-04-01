from rest_framework import permissions


def blog_create_view_permissions_by_action(action):
    if action == 'list':
        return [permissions.AllowAny]
    elif action == 'create':
        return [permissions.IsAuthenticated]
    else:
        return [permissions.IsAuthenticated]
    

def blog_retrieveupdatedelete_permissions_by_action(action):
    if action == 'retrieve':
        return [permissions.AllowAny]
    else:
        return [permissions.IsAuthenticated]