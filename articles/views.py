from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Article


class AllArticlesView(ListView):
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self, **kwargs):
        query = Article.objects.filter(is_published=True)
        query = query.values('pk', 'category__name', 'created', 'title')
        query = query.order_by('-created')
        return query


class ArticleView(DetailView):
    template_name = 'articles/item.html'
    context_object_name = 'article'

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        query = Article.objects.filter(is_published=True, pk=pk)
        if not query.exists():
            raise Http404
        return query