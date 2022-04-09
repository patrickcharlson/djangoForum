from django.conf import settings as forum_settings

from . import defaults


class Settings:

    def __getattr__(self, item):
        try:
            return getattr(forum_settings, item)
        except AttributeError:
            return getattr(defaults, item)
