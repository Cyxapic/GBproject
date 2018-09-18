from django.urls import path, re_path

from . import views


urlpatterns = [
    # re_path(r'^category/(?P<pk>\d+)/$', mainapp.products, name='category'),
    # re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.products, name='page'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('', views.ShopView.as_view(), name='shop'),
]
