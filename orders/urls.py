from django.urls import path

from . import views


urlpatterns = [
    path('create/', views.OrderItemsCreate.as_view(), name='order_create'),
    path('update/<int:pk>/', views.OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', views.OrderDelete.as_view(), name='order_delete'),
    path('read/<int:pk>/', views.OrderRead.as_view(), name='order_read'),
    path('forming/complete/<int:pk>/', views.order_forming_complete, name='order_forming_complete'),
    path('', views.OrderList.as_view(), name='orders_list'),

]
