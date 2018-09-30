
# from django.urls import reverse

# from django.template.loader import render_to_string
# from django.http import JsonResponse

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from shop.models import Product
from .models import Basket


class BasketView(LoginRequiredMixin, ListView):
    template_name = 'basketapp/basket.html'
    context_object_name = 'basket_items'

    def get_queryset(self):
        basket = self.request.user.basket_set.select_related()
        return basket.order_by('product__category')


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)
    basket_item, created = Basket.objects.get_or_create(user=request.user,
                                                        product=product)
    basket_item.quantity += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def basket_remove(request, pk):
#     basket_record = get_object_or_404(Basket, pk=pk)
#     basket_record.delete()
    
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

# @login_required
# def basket_edit(request, pk, quantity):
#     if request.is_ajax():
#         quantity = int(quantity)
#         new_basket_item = Basket.objects.get(pk=int(pk))
            
#         if quantity > 0:
#             new_basket_item.quantity = quantity
#             new_basket_item.save()
#         else:
#             new_basket_item.delete()
            
#         basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
        
#         content = {
#             'basket_items': basket_items,
#         }
        
#         result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        
#         return JsonResponse({'result': result})
#         