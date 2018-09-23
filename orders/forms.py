from django import forms

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemForm(forms.ModelForm):

    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')
        widgets = {
            'product': forms.Select(attrs={'class':'select', }),
            'quantity': forms.NumberInput(attrs={'class': 'input'})
        }
