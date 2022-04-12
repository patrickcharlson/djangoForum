from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturalday
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def profile_link(user):
    data = f'<a href="{reverse("forum:forum_profile", args=[user.username])}">{user.username}</a>'
    return mark_safe(data)


@register.tag
def forum_time(parser, token):
    try:
        tag, time = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('forum_time requires single argument')
    else:
        return ForumTimeNode(time)


class ForumTimeNode(template.Node):
    def __init__(self, time):
        self.time = template.Variable(time)

    def render(self, context):
        time = timezone.localtime(self.time.resolve(context))
        formatted_time = f'{naturalday(time)} {time.strftime("%H:%M:%S")}'
        formatted_time = mark_safe(formatted_time)
        return formatted_time


@register.simple_tag
def link(obj, anchor=''):
    """Return a tag with link to object"""
    url = hasattr(obj, 'get_absolute_url') and obj.get_absolute_url() or None
    anchor = anchor or smart_str(obj)
    return mark_safe(f'<a href="{url}">{escape(anchor)}</a>')


@register.filter
def has_unreads(topic, user):
    ...


@register.simple_tag
def new_reports():
    ...


@register.filter
def forum_unreads(forum, user):
    if not user.is_authenticated:
        return False


@register.simple_tag
def set_theme_style(user):
    selected_theme = ''
    if user.is_authenticated:
        selected_theme = user.forum_profile.theme
        theme_style = '<link rel="stylesheet" type="text/css" href="%(static_url)sforum/themes/%(theme)s/style.css"/>'
    else:
        theme_style = '<link rel="stylesheet" type="text/css" href="%(static_url)sforum/themes/default/style.css"/>'

    return mark_safe(theme_style % dict(
        static_url=settings.STATIC_URL,
        theme=selected_theme
    ))


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
