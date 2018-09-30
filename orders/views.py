from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from django.db import transaction
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DetailView, DeleteView)
from django.forms import inlineformset_factory
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from shop.models import Product
from basketapp.models import Basket
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm



class OrderList(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(LoginRequiredMixin, CreateView):
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
                    form.initial['price'] = basket_items[num].product.price
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
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderItemsUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
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
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderDelete(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('orders:orders_list')

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Order.objects.filter(pk=pk, status=Order.FORMING)


class OrderRead(LoginRequiredMixin, DetailView):
   model = Order


@login_required
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk, status=Order.FORMING)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:orders_list'))


@login_required
def get_price(request):
    pk = request.POST.get('prod_pk')
    price = Product.objects.filter(pk=pk).first().price
    return JsonResponse({'price': price})


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
   if update_fields is 'quantity' or 'product':
       if instance.pk:
           instance.product.quantity -= instance.quantity - \
                                        sender.get_item(instance.pk).quantity
       else:
           instance.product.quantity -= instance.quantity
       instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
   instance.product.quantity += instance.quantity
   instance.product.save()
