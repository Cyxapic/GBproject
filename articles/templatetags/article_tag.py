from django import template


register = template.Library()

@register.simple_tag
def get_thumbnail(article):
    default = '/static/articles/img/troll_face.jpg'
    img = article.articleimage_set.filter(is_title=True).last()
    return img.thumbnail.url if img else default
