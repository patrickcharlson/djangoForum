from django.contrib.auth.models import Group
from django.db import models

from ..models.post import Post
from ..models.topic import Topic


class Category(models.Model):
    name = models.CharField('Name', max_length=80)
    groups = models.ManyToManyField(Group, blank=True, verbose_name='True')
    position = models.IntegerField('Position', blank=True, default=0)

    class Meta:
        db_table = 'categories'
        ordering = ['position']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def forum_count(self):
        return self.forums.all().count()

    @property
    def topics(self):
        return Topic.objects.filter(forum__category__id=self.id).select_related()

    @property
    def posts(self):
        return Post.objects.filter(topic__forum__category__id=self.id).select_related()

    def has_access(self, user):
        if user.is_superuser:
            return True
        if self.groups.exists():
            if user.is_authenticated:
                if not self.groups.filter(user__pk=user.id).exists():
                    return False
            else:
                return False
        return True
