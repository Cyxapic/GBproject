from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('login/', views.GBLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    path('register/', views.RegView.as_view(), name="register"),
    path('edit/', views.EditView.as_view(), name="edit"),
    path('', views.AccountView.as_view(), name="account"),
]