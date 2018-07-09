from django.views.generic import ListView

from articles.models import Article


class IndexView(ListView):
    '''Стартовая страница с последними 10-ю новостями'''
    template_name = "index/index.html"
    context_object_name = 'articles_objects'

    def get_queryset(self, **kwargs):
        query = Article.objects.filter(is_published=True)
        query = query.values('pk', 'created', 'title')
        query = query.order_by('-created')[:10]
        return query
