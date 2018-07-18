from django.urls import reverse
from django.views import View
from django.views.generic import (ListView, DetailView, FormView,
                                  UpdateView, DeleteView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

from .models import Category, Article, ArticleImage
from .forms import ArticleAddForm, ArticleForm, ArticleImageForm


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


class ArticleAdd(LoginRequiredMixin, UserPassesTestMixin, FormView):
    '''Добавляем сатью'''
    template_name = 'articles/add.html'
    form_class = ArticleAddForm

    def form_valid(self, form):
        self.save_article(form)
        messages.success(self.request, 'Запись сохранена!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_add')

    def save_article(self, form):
        article = form.cleaned_data.copy()
        article.pop('image')
        article = Article.objects.create(**article)
        for file in self.request.FILES.getlist('image'):
            print(file)
            image_form = ArticleImageForm(files={'image': file})
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.article = article
                image.save()
            else:
                # need log
                continue

    def test_func(self):
        return self.request.user.is_superuser


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'articles/add.html'
    model = Article
    form_class = ArticleForm
    
    def get_success_url(self):
        return reverse('article_item', kwargs={"pk":self.object.pk})

    def test_func(self):
        return self.request.user.is_superuser


class ArticleDel(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''Удалить запись'''
    model = Article
    success_url='/'

    def test_func(self):
        return self.request.user.is_superuser