from django.urls import reverse
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

from .models import Category, Article, ArticleImage
from .forms import ArticleForm, ArticleImageForm


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
        param = {"is_published": True, "category__pk":cat_pk}
        if self.request.user.is_superuser:
            param = {"category__pk":cat_pk}
        return Article.objects.filter(**param)

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
        param = {"is_published": True, "pk":pk}
        if self.request.user.is_superuser:
            param = {"pk":pk}
        query = Article.objects.filter(**param)
        if not query.exists():
            raise Http404
        return query


class ArticleAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''Добавляем сатью'''
    template_name = 'articles/add.html'
    form_class = ArticleForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Запись сохранена!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_add')

    def test_func(self):
        return self.request.user.is_superuser


class ArticleImageAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''Добавляем изображения к статье'''
    template_name = 'articles/add_image.html'
    form_class = ArticleImageForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Запись сохранена!')
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs['article'] = self.kwargs.get('pk')
        return kwargs

    def get_success_url(self):
        return reverse('article_image', kwargs={'pk':self.kwargs.get('pk')})

    def test_func(self):
        return self.request.user.is_superuser


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'articles/add.html'
    model = Article
    form_class = ArticleForm
    
    def get_success_url(self):
        return reverse('article_item', kwargs={"pk":self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ArticleImage.objects.filter(article__pk=self.object.pk)
        return context

    def test_func(self):
        return self.request.user.is_superuser


class ArticleDel(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''Удалить запись'''
    model = Article
    success_url='/'

    def test_func(self):
        return self.request.user.is_superuser