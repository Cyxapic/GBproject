from django.views.generic import ListView

from articles.models import Article


class IndexView(ListView):
    '''Стартовая страница с последними 9-ю новостями'''
    template_name = "index/index.html"
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        return Article.objects.filter(is_published=True)
