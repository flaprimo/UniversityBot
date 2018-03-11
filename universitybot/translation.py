from functools import wraps
import gettext

_languages = {
    'it': gettext.translation('messages', localedir='locale', languages=['it'])
}


def translate(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        lang = update.message.from_user['language_code'][:2]

        if lang in _languages:
            _languages[lang].install()
        else:
            gettext.install('messages')  # default language

        return func(bot, update, *args, **kwargs)
    return wrapped
