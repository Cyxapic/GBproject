from django.urls import path

from . import views


urlpatterns = [
    path('', views.BasketView.as_view(), name='basket'),
    path('add/<int:pk>/', views.basket_add, name='add'),
    #re_path(r'^remove/(?P<pk>\d+)/$', basketapp.basket_remove, name='remove'),

    #re_path(r'^edit/(?P<pk>\d+)/(?P<quantity>\d+)/$', basketapp.basket_edit, name='edit'),
]

    