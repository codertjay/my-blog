from rest_framework.permissions import BasePermission,SAFE_METHODS

"""
in here we are creating our own permission """


class IsOwnerOrReadonly(BasePermission):
    message = 'You must be the owner of this project '
    # my_safe_methods = ['PUT', 'GET']
    #
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_methods:
    #         return True



    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
