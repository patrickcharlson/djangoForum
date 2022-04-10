from django.db import models

from ..core.conf import settings
from ..models.user import MARKUP_CHOICES


class Post(models.Model):
    topic = models.ForeignKey('forum.Topic', related_name='posts', verbose_name='Topic', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', verbose_name='User',
                             on_delete=models.CASCADE)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Updated by', blank=True, null=True,
                                   related_name='+', on_delete=models.CASCADE)
    markup = models.CharField('Markup', max_length=15, default=settings.DEFAULT_MARKUP, choices=MARKUP_CHOICES)
    body = models.TextField('Message')
    body_html = models.TextField('HTML version')
    user_ip = models.GenericIPAddressField('User IP', blank=True, null=True)

    class Meta:
        db_table = 'posts'
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    @property
    def summary(self):
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or ''
        return self.body[:LIMIT] + tail
