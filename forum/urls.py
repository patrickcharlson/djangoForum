from django.urls import path

from forum import views
from forum.core.feeds import LastPosts, LastTopics, LastPostsOnForum

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/<int:forum_id>/', views.show_forum, name='forum'),

    # Topic
    path('forum/<int:forum_id>/topic/create', views.add_topic, name='add_topic'),

    # User
    path('user/<username>/essentials/', views.user, name='forum_profile_essentials'),
    path('user/<username>/', views.user, name='forum_profile'),
    path('users/', views.users, name='forum_users'),

    # Feeds
    path('feeds/posts/', LastPosts(), name='forum_posts_feed'),
    path('feeds/topics/', LastTopics(), name='forum_topics_feed'),
    path('feeds/forum/<int:forum_id>/', LastPostsOnForum(), name='forum_forum_feed'),

    # Posts
    path('preview/', views.post_preview, name='post_preview')
]
