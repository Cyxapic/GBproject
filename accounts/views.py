from django.views.generic import (CreateView, UpdateView, FormView,
                                  DetailView, TemplateView)
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect

from .forms import LoginForm, RegForm, EditForm, EditExtraForm
from .mixins import RedirectAuthenticatedUserMixin


class GBLoginView(RedirectAuthenticatedUserMixin, FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        self.login_user(form)
        return super().form_valid(form)

    def login_user(self, form):
        login(self.request, form.user_cache,
              backend='django.contrib.auth.backends.ModelBackend')
        expiry = 30 if form.cleaned_data.get("remember") else 0
        self.request.session.set_expiry(expiry)


class RegView(RedirectAuthenticatedUserMixin, CreateView):
    template_name = 'accounts/reg.html'
    form_class = RegForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        messages.success(self.request, 
                         '''Привет, бро!
                            Времена нынче не спокойные!
                            Надо почту подтвердить!''')
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs['domain'] = get_current_site(self.request).name
        return kwargs


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account.html'


class EditView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit.html'
    model = get_user_model()
    form_class = EditForm
    success_url = '/accounts/'

    def form_valid(self, form):
        editextraform = EditExtraForm(self.request.POST,
                                      instance=self.request.user.accountextra)
        if editextraform.is_valid():
            form.save()
        messages.success(self.request, 
                         'Ну вот и все твои данные в сбербанке!')
        return HttpResponseRedirect(self.success_url)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editextraform'] = EditExtraForm(instance=self.request.user.accountextra)
        return context


def account_activate(request, uid, token):
    template = 'accounts/activate.html'
    msg = 'Все пропало!!!'
    user = get_object_or_404(get_user_model(), pk=uid)
    token = default_token_generator.check_token(user, token)
    if token:
        user.is_active = True
        user.save()
        msg = ('Бро, акк активен! '
               'Спасибо за доверие! '
               'Теперь можно читать всякие буквы тут по свойски!')
    messages.success(request, msg)
    return render(request, template)
