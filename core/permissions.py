from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminRole(BasePermission):
    """
    Permite solo a usuarios autenticados con role=ADMIN (o staff) usar mpetodos de escritura-
    Lectura se controla desde el viewset
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (getattr(user, 'role', None) == 'ADMIN' or user.is_staff or user.is_superuser)
        )
    
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS