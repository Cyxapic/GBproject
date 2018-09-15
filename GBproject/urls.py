from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('about/', TemplateView.as_view(template_name="layer/about_temp.html")),
    path('articles/', include(('articles.urls', 'articles'), namespace='articles')),
    path('auth/verify/google/oauth2/', include("social_django.urls", namespace="social")),
    path('', include(('index.urls', 'index'), namespace='index'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
