from social_django.middleware import SocialAuthExceptionMiddleware
from django.shortcuts import redirect
from social_core.exceptions import AuthCanceled


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return redirect('/g-plus/')
