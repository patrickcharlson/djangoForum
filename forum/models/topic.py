from django.conf import settings
from django.db import models


# from forum.models import Post


class Topic(models.Model):
    forum = models.ForeignKey('forum.Forum', related_name='topics', verbose_name='Forum', on_delete=models.CASCADE)
    name = models.CharField('Subject', max_length=255)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    views = models.IntegerField('Views count', blank=True, default=0)
    sticky = models.BooleanField('Sticky', blank=True, default=False)
    closed = models.BooleanField('Closed', blank=True, default=False)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions',
                                         verbose_name='Subscribers', blank=True)
    post_count = models.IntegerField('Post count', blank=True, default=0)
    last_post = models.ForeignKey('forum.Post', related_name='last_topic_post', blank=True, null=True,
                                  on_delete=models.CASCADE)

    class Meta:
        db_table = 'topics'
        ordering = ['-updated']
        get_latest_by = 'updated'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.name

    @property
    def head(self):
        try:
            return self.posts.select_related().order_by('created')[0]
        except IndexError:
            return None
