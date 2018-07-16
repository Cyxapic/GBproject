from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView

from articles.models import Article
from .forms import LoginForm, RegForm


class IndexView(ListView):
    '''Стартовая страница с последними 9-ю новостями'''
    template_name = "index/index.html"
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        return Article.objects.filter(is_published=True)


class GBLoginView(LoginView):
    '''Переопределить форму входа'''
    template_name = "layer/login.html"
    form_class = LoginForm


class RegView(FormView):
    '''регистрация, так как не переопределял модель пользовотеля
       засунул сюда
    '''
    template_name = 'index/reg.html'
    form_class = RegForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 
                         '''Привет, бро!
                            Спасибо за чекин!
                            Теперь можно читать всякие буквы тут по свойски!''')
        return super().form_valid(form)
