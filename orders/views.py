from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.forms import inlineformset_factory

from basketapp.models import Basket
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm



class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm, extra=1)
        basket_items = Basket.get_items(self.request.user)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
            # Удаляем корзину только при POST - иначе теряем заказ
            basket_items.delete()
        else:
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderDelete(DeleteView):
    success_url = reverse_lazy('orders:orders_list')

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Order.objects.filter(pk=pk, status=Order.FORMING)


class OrderRead(DetailView):
   model = Order


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk, status=Order.FORMING)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:orders_list'))
