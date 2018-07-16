from django.urls import path

from . import views


urlpatterns = [
    path('article/<int:pk>/', views.ArticleView.as_view(), name='article_item'),
    path('<int:cat_pk>/', views.CategoriesItems.as_view(), name='categories_items'),
    path('', views.AllCategoriesView.as_view(), name='categories'),
]