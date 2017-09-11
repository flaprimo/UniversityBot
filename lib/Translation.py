import gettext

_languages = {
    'it': gettext.translation('messages', localedir='locale', languages=['it'])
}


def translate(lang):
    lang = lang[:2]
    if lang in _languages:
        _languages[lang].install()
    else:
        gettext.install("messages")  # default language
