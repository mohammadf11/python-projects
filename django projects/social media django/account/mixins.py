from django.shortcuts import redirect
from . models import Profile
class LogoutRequirementMixin():
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('social_media:home')
            
class ProfileMixin():
    def dispatch(self, request, *args, **kwargs):

        return super(CLASS_NAME, self).dispatch(request, *args, **kwargs)
