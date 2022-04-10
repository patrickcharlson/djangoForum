from django.db import models
from django.urls import reverse

from ..core.conf import settings
from ..core.fields import ExtendedImageField
from ..models.post import Post


class Forum(models.Model):
    category = models.ForeignKey('forum.Category', related_name='forums', verbose_name='Category',
                                 on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=80)
    position = models.IntegerField('Position', blank=True, default=0)
    description = models.TextField('Description', blank=True, default='')
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='Moderators')
    updated = models.DateTimeField('Updated', auto_now=True)
    post_count = models.IntegerField('Post count', blank=True, default=0)
    topic_count = models.IntegerField('Topic count', blank=True, default=0)
    last_post = models.ForeignKey('Post', related_name='last_forum_post', blank=True, null=True,
                                  on_delete=models.CASCADE)
    forum_logo = ExtendedImageField('Forum Logo', blank=True, default='',
                                    upload_to=settings.FORUM_LOGO_UPLOAD_TO,
                                    width=settings.FORUM_LOGO_WIDTH,
                                    height=settings.FORUM_LOGO_HEIGHT)

    class Meta:
        db_table = 'forums'
        ordering = ['position']
        verbose_name = 'Forum'
        verbose_name_plural = 'Forums'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum:forum', args=[self.id])

    @property
    def posts(self):
        return Post.objects.filter(topic__forum__id=self.id).select_related()
