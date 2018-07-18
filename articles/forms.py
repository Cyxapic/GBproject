from django import forms

from .models import Category, Article, ArticleImage


class ArticleAddForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "input"}))
    text = forms.CharField(widget=forms.Textarea())
    is_published = forms.BooleanField(required=False)
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
                attrs={'multiple': True, "class":"file-input"}
            )
        )


class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = ('image',)


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "input"}))
    text = forms.CharField(widget=forms.Textarea())
    is_published = forms.BooleanField(required=False)

    class Meta:
        model = Article
        fields = ('category', 'title', 'text', 'is_published',)