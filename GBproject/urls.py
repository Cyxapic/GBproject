from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name="layer/login.html")),
    path('logout/', LogoutView.as_view(template_name="layer/logout.html")),
    path('about/', TemplateView.as_view(template_name="layer/about_temp.html")),
    path('articles/', include('articles.urls')),
    path('', include('index.urls'))
]