from django import template


register = template.Library()


@register.simple_tag
def likes(user):
    return user.like_set.likes(user)
