from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.views import LoginView

from .forms import LoginForm, RegForm


class GBLoginView(LoginView):
    '''Переопределить форму входа'''
    template_name = "accounts/login.html"
    form_class = LoginForm


class RegView(CreateView):
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
