import os

import pytz
from django.db import models

from ..core.conf import settings
from ..core.fields import ExtendedImageField, AutoOneToOneField

TZ_CHOICES = [(tz_name, tz_name) for tz_name in pytz.common_timezones]

PRIVACY_CHOICES = (
    (0, 'Display your e-mail address.'),
    (1, 'Hide your e-mail address but allow form e-mail.'),
    (2, 'Hide your e-mail address and disallow form e-mail.'),
)

MARKUP_CHOICES = [('bbcode', 'bbcode')]
try:
    import markdown

    MARKUP_CHOICES.append(("markdown", "markdown"))
except ImportError:
    pass

path = os.path.join(settings.STATIC_ROOT, 'forum', 'themes')
if os.path.exists(path):
    # fix for collect-static
    THEME_CHOICES = [(theme, theme) for theme in os.listdir(path)
                     if os.path.isdir(os.path.join(path, theme))]
else:
    THEME_CHOICES = []


class ProfileManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        qs = super().get_queryset()
        if settings.REPUTATION_SUPPORT:
            qs = qs.extra(select={
                'reply_total': 'SELECT SUM(sign) FROM reputations WHERE to_user_id = '
                               'users.user_id GROUP BY to_user_id',

                'reply_count_minus': "SELECT SUM(sign) FROM reputations WHERE to_user_id = "
                                     "users.user_id AND sign = '-1' GROUP BY to_user_id",

                'reply_count_plus': "SELECT SUM(sign) FROM reputations WHERE to_user_id = "
                                    "users.user_id AND sign = '1' GROUP BY to_user_id",
            })
        return qs


class Profile(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, related_name='forum_profile', verbose_name='User',
                             on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=30, blank=True)
    site = models.URLField('Site', blank=True)
    jabber = models.CharField('Jabber', max_length=80, blank=True)
    icq = models.CharField('ICQ', max_length=12, blank=True)
    msn = models.CharField('MSN', max_length=80, blank=True)
    aim = models.CharField('AIM', max_length=80, blank=True)
    yahoo = models.CharField('Yahoo', max_length=80, blank=True)
    location = models.CharField('Location', max_length=30, blank=True)
    signature = models.TextField('Signature', blank=True, default='', max_length=settings.SIGNATURE_MAX_LENGTH)
    signature_html = models.TextField('Signature', blank=True, default='',
                                      max_length=settings.SIGNATURE_MAX_LENGTH)
    time_zone = models.CharField('Time zone', max_length=50, choices=TZ_CHOICES, default=settings.TIME_ZONE)
    language = models.CharField('Language', max_length=7, default='', choices=settings.LANGUAGES)
    avatar = ExtendedImageField('Avatar', blank=True, default='', upload_to=settings.AVATARS_UPLOAD_TO,
                                width=settings.AVATAR_WIDTH, height=settings.AVATAR_HEIGHT)
    theme = models.CharField('Theme', choices=THEME_CHOICES, max_length=80, default='default')
    show_avatar = models.BooleanField('Show avatar', blank=True, default=True)
    show_signatures = models.BooleanField('Show signatures', blank=True, default=True)
    show_smilies = models.BooleanField('Show smilies', blank=True, default=True)
    privacy_permission = models.IntegerField('Privacy permission', choices=PRIVACY_CHOICES, default=1)
    auto_subscribe = models.BooleanField('Auto subscribe',
                                         help_text="Auto subscribe all topics you have created or reply.",
                                         blank=True, default=False)
    markup = models.CharField('Default markup', max_length=15, default=settings.DEFAULT_MARKUP,
                              choices=MARKUP_CHOICES)
    post_count = models.IntegerField('Post count', blank=True, default=0)

    objects = ProfileManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
