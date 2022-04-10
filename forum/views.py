from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from forum.core.conf import settings
from forum.core.utils import convert_text_to_html, smiles, get_page
from forum.models import Forum, Post, Category

User = get_user_model()


def index(request):
    users_cached = cache.get('forum_users_online', {})
    users_online = users_cached and User.objects.filter(id__in=users_cached.keys()) or []
    guests_cached = cache.get('forum_guests_online', {})
    guests_count = len(guests_cached)
    users_count = len(users_online)

    forums = Forum.objects.all()
    user = request.user
    if not user.is_superuser:
        user_groups = user.groups.all() or []
        forums = forums.filter(Q(category__groups__in=user_groups) | Q(category__groups__isnull=True))
    forums = forums.select_related('last_post__topic', 'last_post__user', 'category')

    categories = {}
    forum_dict = {}
    for forum in forums:
        category = categories.setdefault(forum.category.id,
                                         {'id': forum.category.id, 'category': forum.category, 'forums': []})

        category['forums'].append(forum)
        forum_dict[forum.id] = forum

    categories = sorted(categories.values(), key=lambda x: x['category'].position)

    context = {
        'categories': categories,
        'posts': Post.objects.count(),
        'users': User.objects.count(),
        'users_online': users_online,
        'online_count': users_count,
        'guest_count': guests_count,
        'last_user': User.objects.latest('date_joined')
    }
    return render(request, 'forum/index.html', context)


def show_forum(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    if not forum.category.has_access(request.user):
        raise PermissionDenied
    topics = forum.topics.order_by('-sticky', '-updated').select_related()
    moderator = request.user.is_superuser or request.user in forum.moderators.all()

    categories = []
    for category in Category.objects.all():
        if category.has_access(request.user):
            categories.append(category)

    context = {
        'categories': categories,
        'forum': forum,
        'posts': forum.post_count,
        'topics_page': get_page(topics, request, settings.FORUM_PAGE_SIZE),
        'moderator': moderator
    }

    return render(request, 'forum/forum.html', context)


def post_preview(request):
    """Preview for markitup"""

    markup = request.user.forum_profile.markup
    data = request.POST.get('data', '')

    data = convert_text_to_html(data, markup)
    if settings.SMILES_SUPPORT:
        data = smiles(data)
    context = {'data': data}
    return render(request, 'forum/post_preview.html', context)
