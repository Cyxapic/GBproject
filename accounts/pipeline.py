import re

from social_core.exceptions import AuthForbidden


pattern = r'&\w+;\w+&\w+;'
GENDER = (
    'other',
    'male',
    'female',
)


def social_user_save(backend, user, response, *args, **kwargs):
    """save user from social apps"""
    if backend.name == 'google-oauth2':
        user.is_active = True
        if not user.birthday and 'birthday' in response:
            user.birthday = response['birthday']
        user.image = response['image']['url']
        if response['isPlusUser']:
            user.accountextra.g_plus = response.get('url')
            user.accountextra.gender = GENDER.index(response.get('gender', 0))
            if not user.accountextra.about:
                about = re.sub(pattern, '', response.get('aboutMe', ''))
                user.accountextra.about = about
        else:
            raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()
