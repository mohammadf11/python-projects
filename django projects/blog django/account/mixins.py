from django.core.exceptions import PermissionDenied

class SuperuserAuthorAccessMixins:
    def dispatch(self, request, *args, **kwargs):
        if  request.user.is_author or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
            

class SuperuserAccessMixins:
    def dispatch(self, request, *args, **kwargs):
        if  request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
        
