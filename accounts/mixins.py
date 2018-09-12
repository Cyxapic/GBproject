from django.shortcuts import redirect
from django.conf import settings


class RedirectAuthenticatedUserMixin:
    def dispatch(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, **kwargs)
