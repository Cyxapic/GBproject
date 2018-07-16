from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Category, Article


class AllCategoriesView(ListView):
    '''Вывести все категории'''
    template_name = 'articles/index.html'
    model = Category
    context_object_name = 'categories'
    paginate_by = 9


class CategoriesItems(ListView):
    '''Вывести все записи категории > category.pk'''
    template_name = 'articles/categories_items.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        cat_pk = self.kwargs.get('cat_pk')
        query = Article.objects.filter(is_published=True, category__pk=cat_pk)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('cat_pk')
        context['category'] = Category.objects.get(pk=pk)
        return context


class ArticleView(DetailView):
    '''Вывести запись'''
    template_name = 'articles/item.html'
    context_object_name = 'article'

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        query = Article.objects.filter(is_published=True, pk=pk)
        if not query.exists():
            raise Http404
        return query