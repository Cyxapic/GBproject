from django import forms

from .models import Category, Article, ArticleImage


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            empty_label='Категория')
    title = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "input",
                       "placeholder": "Название записи..."}))
    text = forms.CharField(widget=forms.Textarea())
    is_published = forms.BooleanField(required=False)

    class Meta:
        model = Article
        fields = ('category', 'title', 'text', 'is_published',)


class ArticleImageForm(forms.ModelForm):
    def __init__(self, **kwargs):
        self.article = kwargs.pop('article', None)
        super().__init__(**kwargs)

    class Meta:
        model = ArticleImage
        fields = ('image', 'is_title')
        widgets = {
            'image': forms.ClearableFileInput(attrs={"class":"file-input",
                                                     "required": True}),
            'is_title': forms.CheckboxInput(attrs={"class":"titul-img"})
        }

    def save(self, commit=True):
        article = Article.objects.get(pk=self.article)
        image = super().save(commit=False)
        image.article = article
        if commit:
            image.save()
        return image
