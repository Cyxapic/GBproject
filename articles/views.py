import json

from django.urls import reverse
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Category, Article, ArticleImage, Like
from .forms import CategoryAddForm, ArticleForm, ArticleImageForm


class AllCategoriesView(ListView):
    '''Вывести все категории'''
    template_name = 'articles/index.html'
    model = Category
    context_object_name = 'categories'
    paginate_by = 8


class CategoriesItems(ListView):
    '''Вывести все записи категории > category.pk'''
    template_name = 'articles/categories_items.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        cat_pk = self.kwargs.get('cat_pk')
        param = {"is_published": True, "category__pk":cat_pk}
        if self.request.user.is_staff:
            param = {"category__pk":cat_pk}
        return Article.objects.filter(**param)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('cat_pk')
        context['category'] = Category.objects.get(pk=pk)
        return context


class ArticleView(DetailView):
    '''Вывести запись'''
    template_name = 'articles/article.html'
    context_object_name = 'article'

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        param = {"is_published": True, "pk":pk}
        if self.request.user.is_staff:
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
        return reverse('articles:article_edit', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.is_staff


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
        return reverse('articles:article_edit', kwargs={'pk':self.kwargs.get('pk')})

    def test_func(self):
        return self.request.user.is_staff


class ArticleImageDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''Добавляем изображения к статье'''
    model = ArticleImage

    def get_success_url(self):
        article = self.request.POST.get('article')
        return reverse('articles:article_edit', kwargs={'pk':article})

    def test_func(self):
        return self.request.user.is_staff


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'articles/add.html'
    model = Article
    form_class = ArticleForm
    
    def get_success_url(self):
        return reverse('articles:article_item', kwargs={"pk":self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ArticleImage.objects.filter(article__pk=self.object.pk)
        return context

    def test_func(self):
        return self.request.user.is_staff


class ArticleDel(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''Удалить запись'''
    model = Article
    success_url='/'

    def test_func(self):
        return self.request.user.is_staff

@login_required
def category_add(request):
    resp = {'error': None}
    if request.method == "POST":
        data = json.loads(request.body)
        form = CategoryAddForm(data)
        if form.is_valid():
            cat = form.save()
            resp.update({'pk': cat.pk, 'name': cat.name})
        else:
            resp["error"] = "Ошибка создания категории!"
    return JsonResponse(resp)


@login_required
def like_article(request, pk):
    resp = {'error': None}
    if request.method == "POST":
        user = request.user
        article = get_object_or_404(Article, pk=pk)
        _, created = Like.objects.get_or_create(user=user, article=article)
        if  created:
            resp['count'] = Like.objects.article_likes(article)
        else:
            resp['error'] = 400
    return JsonResponse(resp)