from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from articles.models import Article


class IndexView(ListView):
    '''Стартовая страница с последними 9-ю новостями'''
    template_name = "index/index.html"
    context_object_name = 'articles'

    def get_queryset(self, **kwargs):
        query = Article.objects.filter(is_published=True)
        query = query.order_by('-created')[:6]
        return query


class RegView(FormView):
    template_name = 'index/reg.html'
    form_class = UserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 
                         '''Привет, бро!
                            Спасибо за чекин!
                            Теперь можно читать всякие буквы тут по свойски!''')
        return super().form_valid(form)
