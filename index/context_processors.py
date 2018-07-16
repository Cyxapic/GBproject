import re

from django.urls import reverse

from .models import MainMenu


def menus(request):
    menus = MainMenu.objects.exclude(posnum=0).values('url', 'title')
    for menu in menus:
        if match_url(reverse(menu["url"]), request.path):
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