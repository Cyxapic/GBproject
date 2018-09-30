from django.views.generic import ListView, DetailView

from .models import ProductCategory, Product


class ShopView(ListView):
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    paginate_by = 3

    def get_queryset(self):
        queryset = {'is_active': True,
                    'category__is_active': True}
        category = self.get_filter()
        if category:
            queryset.update(category)
        products = Product.objects.filter(**queryset)
        return products.select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = ProductCategory.objects.all()
        context['categories'] = category.values_list('pk' ,'name')
        category = self.get_filter()
        if category:
            context.update(category)
        return context

    def get_filter(self):
        category = self.request.GET.get('category')
        if category and category.isdigit():
            category = {'category': category}
        else:
            category = None
        return category


class ProductView(DetailView):
    template_name = 'shop/product.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(pk=pk,
                                         is_active=True,
                                         category__is_active=True)
        return product.select_related()
