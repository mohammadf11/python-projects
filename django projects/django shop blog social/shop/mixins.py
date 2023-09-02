from django.core.exceptions import PermissionDenied
class IsStaffAccessMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    