from django.views.generic import ListView, DetailView

from .models import ProductCategory, Product


class ShopView(ListView):
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    paginate_by = 3

    def get_queryset(self):
        products = Product.objects.filter(is_active=True,
                                          category__is_active=True)
        return products


class ProductView(DetailView):
    template_name = 'shop/product.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(pk=pk,
                                         is_active=True,
                                         category__is_active=True)
        return product