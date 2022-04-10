from django.urls import path

from forum import views
from forum.feeds import LastPosts, LastTopics, LastPostsOnForum

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/<int:forum_id>/', views.show_forum, name='forum'),

    # Feeds
    path('feeds/posts/', LastPosts(), name='forum_posts_feed'),
    path('feeds/topics/', LastTopics(), name='forum_topics_feed'),
    path('feeds/forum/<int:forum_id>/', LastPostsOnForum(), name='forum_forum_feed'),

    # Posts
    path('preview/', views.post_preview, name='post_preview')
]
