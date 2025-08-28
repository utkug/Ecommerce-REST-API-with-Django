from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)#True and False
        return request.method in permissions.SAFE_METHODS or is_admin

class IsOwnerProductOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.seller.user
            
class IsOwnerStoreOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
    

class IsStoreOrCustomer(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return request.user.is_store
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_store
    

class IsStoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.product.seller.user

        
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer and hasattr(request.user, 'customer')
    
class IsStore(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_store