from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import Forum, Post, Topic


class ForumFeed(Feed):
    feed_type = Atom1Feed

    def link(self):
        return reverse('forum:index')

    def item_guild(self, obj):
        return str(obj.id)

    def item_author_name(self, item):
        return item.user.username


class LastPosts(ForumFeed):
    title = 'Latest posts on forum'
    description = 'Latest posts on forum'
    title_template = 'forum/feeds/posts_title.html'
    description_template = 'forum/feeds/posts_description.html'

    def get_object(self, request, *args, **kwargs):
        user_groups = request.user.groups.all()
        if request.user.is_anonymous:
            user_groups = []
        allow_forums = Forum.objects.filter(
            Q(category__groups__in=user_groups) | Q(category__groups__isnull=True))
        return allow_forums

    def items(self, allow_forums):
        return Post.objects.filter(topic__forum__in=allow_forums).order_by('-created')[:15]


class LastTopics(ForumFeed):
    title = 'Latest topics on forum'
    description = 'Latest topics on forum'
    title_template = 'forum/feeds/topics_title.html'
    description_template = 'forum/feeds/topics_description.html'

    def get_object(self, request, *args, **kwargs):
        user_groups = request.user.groups.all()
        if request.user.is_anonymous():
            user_groups = []
        allow_forums = Forum.objects.filter(
            Q(category__groups__in=user_groups) | Q(category__groups__isnull=True))
        return allow_forums

    def items(self, allow_forums):
        return Topic.objects.filter(forum__in=allow_forums).order_by('-created')[:15]
