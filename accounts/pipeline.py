def social_user_activate(backend, user, response, *args, **kwargs):
    user.is_active = True
    user.save()