import re

from django.urls import reverse, NoReverseMatch

from .models import MainMenu


def menus(request):
    menus = MainMenu.objects.exclude(posnum=0).values('url', 'title')
    for menu in menus:
        try:
            url = reverse(menu["url"])
        except NoReverseMatch:
            # Позже привяжу логирование
            continue
        if match_url(url, request.path):
            menu["style"] = "menu-active"
        else:
            menu["style"] = None
    return {"menus": menus}


def match_url(url, current_url):
    if re.match(r"%s\d+/$"%url, current_url):
        return True
    elif re.match(r"%s$"%url, current_url):
        return True
    return False