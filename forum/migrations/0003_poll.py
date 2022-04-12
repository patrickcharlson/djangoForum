# Generated by Django 4.0.3 on 2022-04-10 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('choice_count', models.PositiveSmallIntegerField(default=1, help_text='How many choices are you allowed simultaneously')),
                ('active', models.BooleanField(default=True, help_text='Can users vote to this poll or just see the result?')),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='Point of time after this poll would be automatically deactivated', null=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='forum.topic', verbose_name='Poll')),
                ('users', models.ManyToManyField(blank=True, help_text='Users who have voted on this poll', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
                'db_table': 'polls',
            },
        ),
    ]