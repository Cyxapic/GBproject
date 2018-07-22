from django.urls import path

from . import views


urlpatterns = [
    path('article/add/', views.ArticleAdd.as_view(), name='article_add'),
    path('article/edit/<int:pk>/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('article/image/<int:pk>/', views.ArticleImageAdd.as_view(), name='article_image'),
    path('article/delete/<int:pk>/', views.ArticleDel.as_view(), name='article_del'),
    path('article/<int:pk>/', views.ArticleView.as_view(), name='article_item'),
    path('<int:cat_pk>/', views.CategoriesItems.as_view(), name='categories_items'),
    path('', views.AllCategoriesView.as_view(), name='categories'),
]