from django.shortcuts import reverse

def menus(request):
    '''Можно потом в БД засунуть, чтобы править проще было'''
    menu_data = [
                    {"url":"home",
                     "name": "Наиглавнейшая",
                     "style": None,},
                    {"url":"all_articles",
                     "name": "Записки о всяком",
                     "style": None,}
                ]
    for menu in menu_data:
        if reverse(menu["url"]) == request.path:
            menu["style"] = "is-active"
        else:
            menu["style"] = None
    return {"menus": menu_data}
