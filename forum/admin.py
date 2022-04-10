from django.contrib import admin

from .models import Post, Topic, Forum, Category


class BaseModelAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        # disabled, because delete_selected ignoring delete model method
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    list_display = ['name', 'position', 'forum_count']


@admin.register(Forum)
class ForumAdmin(BaseModelAdmin):
    list_display = ['name', 'category', 'position', 'topic_count']
    raw_id_fields = ['moderators', 'last_post']


@admin.register(Topic)
class TopicAdmin(BaseModelAdmin):
    def subscribers2(self, obj):
        return ", ".join([user.username for user in obj.subscribers.all()])

    subscribers2.short_description = "subscribers"

    list_display = ['name', 'forum', 'created', 'head', 'post_count', 'subscribers2']
    search_fields = ['name']
    raw_id_fields = ['user', 'subscribers', 'last_post']


@admin.register(Post)
class PostAdmin(BaseModelAdmin):
    list_display = ['topic', 'user', 'created', 'updated', 'summary']
    search_fields = ['body']
    raw_id_fields = ['topic', 'user', 'updated_by']
