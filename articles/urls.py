from django.urls import path

from . import views


urlpatterns = [
    path('<int:pk>/', views.ArticleView.as_view(), name='article_item'),
    path('', views.AllArticlesView.as_view(), name='all_articles'),
]