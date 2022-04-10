from forum.core.conf import settings


def forum_settings(request):
    return {
        'forum_settings': settings,
        'DEBUG': settings.DEBUG
    }
