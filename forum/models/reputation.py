from django.conf import settings
from django.db import models


class Reputation(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reputations_from', verbose_name='From')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reputations_to', verbose_name='To')
    post = models.ForeignKey('forum.Post', related_name='post', verbose_name='Post', on_delete=models.CASCADE)
    time = models.DateTimeField('Time', auto_now_add=True)
    sign = models.IntegerField('Sign', choices=SIGN_CHOICES, default=0)
    reason = models.TextField('Reason', max_length=1000)
