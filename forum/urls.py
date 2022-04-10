from django.urls import path

from forum import views
from forum.feeds import LastPosts, LastTopics

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),

    # Feeds
    path('feeds/posts/', LastPosts(), name='forum_posts_feed'),
    path('feeds/topics/', LastTopics(), name='forum_topics_feed'),

    # Posts
    path('preview/', views.post_preview, name='post_preview')
]
