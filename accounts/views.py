from django.views.generic import (CreateView, UpdateView,
                                 DetailView, TemplateView)
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import LoginForm, RegForm, EditForm
from .mixins import RedirectAuthenticatedUserMixin


class GBLoginView(RedirectAuthenticatedUserMixin, LoginView):
    '''Переопределить форму входа'''
    template_name = "accounts/login.html"
    form_class = LoginForm


class RegView(RedirectAuthenticatedUserMixin, CreateView):
    template_name = 'accounts/reg.html'
    form_class = RegForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 
                         '''Привет, бро!
                            Спасибо за чекин!
                            Теперь можно читать всякие буквы тут по свойски!''')
        return super().form_valid(form)


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account.html'


class EditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit.html'
    model = get_user_model()
    form_class = EditForm
    success_url = '/accounts/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 
                         '''Ну вот и все твои данные в сбербанке!''')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user
