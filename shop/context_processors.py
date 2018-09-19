from basketapp.models import Basket


def basket(request):
    basket = Basket.objects.filter(user=request.user)
    basket = basket if basket else ''
    return {
        'basket': basket,
    }
