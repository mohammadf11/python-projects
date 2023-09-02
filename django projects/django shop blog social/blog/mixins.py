from django.core.exceptions import PermissionDenied
from .models import Article
class IsSuperuserOrOwnerAccessMixins():
    def dispatch(self, request, *args, **kwargs):
        article = Article.objects.get(id = kwargs['pk'])
        if request.user.is_superuser or article.author==request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

class IsStaffAccessMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    