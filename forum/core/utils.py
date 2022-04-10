from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import List, Tuple

import markdown
from django.core.paginator import Paginator, InvalidPage
from django.utils.html import urlize

from forum.core.conf import settings

_SMILES = [(re.compile(smile_re), path) for smile_re, path in settings.SMILES]


class HTMLParseError(Exception):
    ...


def get_page(objects, request, size):
    try:
        return Paginator(objects, size).page(request.GET.get('page', 1))
    except InvalidPage:
        return None


def build_form(Form, request, GET=False, *args, **kwargs):
    if not GET and 'POST' == request.method:
        form = Form(request.POST, request.FILES, *args, **kwargs)
    elif GET and 'GET' == request.method:
        form = Form(request.GET, request.FILES, *args, **kwargs)
    else:
        form = Form(*args, **kwargs)
    return form


class HTMLFilter(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.convert_charrefs = False
        self.html = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        self.html.append(f'<{tag}{self.__html_attrs(attrs)}>')

    def handle_endtag(self, tag: str) -> None:
        self.html.append(f'</{tag}>')

    def handle_entityref(self, name: str) -> None:
        self.html.append(f'&{name}')

    def handle_charref(self, name: str) -> None:
        self.html.append(f'&#{name}')

    def unescape(self, s):
        return s

    def __html_attrs(self, attrs):
        _attrs = ''
        if attrs:
            _attrs = ' %s' % (' '.join([f'{k}="{v}"' for k, v in attrs]))
        return _attrs

    def feed(self, data: str) -> None:
        HTMLParser.feed(self, data)
        self.html = ''.join(self.html)


class ExcludeTagsHTMLFilter(HTMLFilter):
    """Class for html parsing with excluding specified tags"""

    def __init__(self, func, tags=('a', 'pre', 'span')):
        HTMLFilter.__init__(self)
        self.func = func
        self.is_ignored = False
        self.tags = tags

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        if tag in self.tags:
            self.is_ignored = True
        HTMLFilter.handle_starttag(self, tag, attrs)

    def handle_data(self, data: str) -> None:
        if not self.is_ignored:
            data = self.func(data)
        HTMLFilter.handle_data(self, data)

    def handle_endtag(self, tag: str) -> None:
        self.is_ignored = False
        HTMLFilter.handle_endtag(self, tag)


def _smile_replacer(data):
    for smile, path in _SMILES:
        data = smile.sub(path, data)
    return data


def smiles(html):
    """Replace text smiles"""

    try:
        parser = ExcludeTagsHTMLFilter(_smile_replacer)
        parser.feed(html)
        smiled_html = parser.html
        parser.close()
    except HTMLParseError:
        if settings.DEBUG:
            raise
        return html
    return smiled_html


class AddAttributesHTMLFilter(HTMLFilter):

    def __init__(self, add_attr_map):
        HTMLFilter.__init__(self)
        self.add_attr_map = dict(add_attr_map)

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        attrs = list(attrs)
        for add_attr in self.add_attr_map.get(tag, []):
            if add_attr not in attrs:
                attrs.append(add_attr)

        HTMLFilter.handle_starttag(self, tag, attrs)


def add_rel_nofollow(html):
    try:
        parser = AddAttributesHTMLFilter({'a': [('rel', 'nofollow')]})
        parser.feed(html)
        output_html = parser.html
        parser.close()
    except HTMLParseError:
        if settings.DEBUG:
            raise
        return html
    return output_html


def convert_text_to_html(text, markup):
    if markup == 'bbcode':
        text = render_bbcode(text)
    elif markup == 'markdown':
        text = markdown.markdown(text, safe_mode='escape')
    else:
        raise Exception('Invalid markup property: %s' % markup)
    text = urlize(text)
    if settings.NOFOLLOW_LINKS:
        text = add_rel_nofollow(text)
    return text
