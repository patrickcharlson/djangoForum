from django.conf import settings
from django.db import models
from django.db.models import aggregates
from django.utils import timezone


class Poll(models.Model):
    topic = models.ForeignKey('forum.Topic', on_delete=models.CASCADE, verbose_name='Poll', related_name='polls')
    question = models.CharField(max_length=200)
    choice_count = models.PositiveSmallIntegerField(default=1,
                                                    help_text='How many choices are you allowed simultaneously')
    active = models.BooleanField(default=True, help_text='Can users vote to this poll or just see the result?')
    deactivate_date = models.DateTimeField(null=True, blank=True,
                                           help_text='Point of time after this poll would be automatically deactivated')

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text='Users who have voted on this poll')

    class Meta:
        db_table = 'polls'
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return self.question

    def deactivate_if_expired(self):
        if self.active and self.deactivate_date:
            now = timezone.now()
            if now > self.deactivate_date:
                self.active = False
                self.save()

    def single_choice(self):
        return self.choice_count == 1


class PollChoice(models.Model):
    poll = models.ForeignKey('forum.Poll', related_name='choices', on_delete=models.CASCADE, verbose_name='Poll')
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, editable=False)

    def percent(self):
        if not self.votes:
            return 0.0
        result = PollChoice.objects.filter(poll=self.poll).aggregate(aggregates.Sum('votes'))
        votes_sum = result['votes__sum']
        return float(self.votes) / votes_sum * 100

    def __str__(self):
        return self.choice
