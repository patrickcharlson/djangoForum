from datetime import timedelta

from django import forms
from django.utils import timezone

from forum.core.conf import settings
from forum.core.utils import set_language
from forum.models import Profile, Post, Poll, PollChoice

SORT_USER_BY_CHOICES = (
    ('username', 'Username'),
    ('registered', 'Registered'),
    ('num_posts', 'No. of posts'),
)

SORT_DIR_CHOICES = (
    ('ASC', 'Ascending'),
    ('DESC', 'Descending'),
)


class EssentialsProfileForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='Email')

    class Meta:
        model = Profile
        fields = ['auto_subscribe', 'time_zone', 'language']

    def __init__(self, *args, **kwargs):
        extra_args = kwargs.pop('extra_args', {})
        self.request = extra_args.pop('request', None)
        self.profile = kwargs['instance']
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.profile.user.username
        if not self.request.user.is_superuser:
            self.fields['username'].widget = forms.HiddenInput()
        self.fields['email'].initial = self.profile.user.email

    def save(self, commit=True):
        if self.cleaned_data:
            if self.request.user.is_superuser:
                self.profile.user.username = self.cleaned_data['username']
            self.profile.user.email = self.cleaned_data['email']
            self.profile.time_zone = self.cleaned_data['time_zone']
            self.profile.language = self.cleaned_data['language']
            self.profile.user.save()
            if commit:
                self.profile.save()
        set_language(self.request, self.profile.language)
        return self.profile


class PollForm(forms.ModelForm):
    question = forms.CharField(label='Question')
    answers = forms.CharField(label='Answers', min_length=2, widget=forms.Textarea,
                              help_text='Write each answer on a new line')
    days = forms.IntegerField(label='Days', required=False, min_value=1,
                              help_text='Number of days for this poll to run. Leave empty for never ending poll')
    choice_count = forms.IntegerField(label='Choice Count', required=True, initial=1, min_value=1,
                                      error_messages={'min_value': "Number of choices must be positive."})

    class Meta:
        model = Poll
        fields = ['question', 'choice_count']

    def has_data(self):
        return any(self.data.get(key) for key in ('question', 'answers', 'days'))

    # def clean_answers(self):
    #     raw_answers = self.cleaned_data['answers']
    #     answers = [answer.strip() for answer in raw_answers.splitlines() if answer.strip()]
    #     if answers:
    #         raise forms.ValidationError('There is no valid answer!')
    #
    #     is_max_length = max([len(answer) for answer in answers])
    #     should_max_length = PollChoice._meta.get_field('choice').max_length
    #     if is_max_length > should_max_length:
    #         raise forms.ValidationError('One of this answers are too long')
    #
    #     return answers

    def save(self, post):
        poll = super().save(commit=False)
        poll.topic = post.topic
        days = self.cleaned_data['days']
        if days:
            poll.deactivate_date = timezone.now() + timedelta(days=days)
        poll.save()
        answers = self.cleaned_data['answers']
        for answer in answers:
            PollChoice.objects.create(poll=poll, choice=answer)


class AddPostForm(forms.ModelForm):
    form_name = 'AddPostForm'

    name = forms.CharField(label='Subject', max_length=255, widget=forms.TextInput(attrs={'size': '115'}))
    attachment = forms.FileField(label='Attachment', required=False)
    subscribe = forms.BooleanField(label='Subscribe', help_text='Subscribe this topic', required=False)

    class Meta:
        model = Post
        fields = ['body']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.topic = kwargs.pop('topic', None)
        self.forum = kwargs.pop('forum', None)
        self.ip = kwargs.pop('ip', None)
        super().__init__(*args, **kwargs)

        if self.topic:
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['name'].required = False

        self.fields['body'].widget = forms.Textarea(attrs={'class': 'markup', 'rows': '20', 'cols': '95'})

    def clean(self):
        error_msg = 'Can\'t be empty nor contain only whitespace characters'
        cleaned_data = self.cleaned_data
        body = cleaned_data.get('body')
        subject = cleaned_data.get('name')
        if subject:
            if not subject.strip():
                self._errors['name'] = self.error_class([error_msg])
                del cleaned_data['name']
        if body:
            if not body.strip():
                self._errors['body'] = self.error_class([error_msg])
                del cleaned_data['body']
        return cleaned_data

    def save(self):
        if self.


class UserSearchForm(forms.Form):
    username = forms.CharField(required=False, label='Username')
    sort_by = forms.ChoiceField(choices=SORT_USER_BY_CHOICES, label='Sort by')
    sort_dir = forms.ChoiceField(choices=SORT_DIR_CHOICES, label='Sort Order')

    def filter(self, qs):
        if self.is_valid():
            username = self.cleaned_data['username']
            sort_by = self.cleaned_data['sort_by']
            sort_dir = self.cleaned_data['sort_dir']
            qs = qs.filter(username__contains=username, forum_profile__post_count__gte=settings.POST_USER_SEARCH)
            if sort_by == 'username':
                if sort_dir == 'ASC':
                    return qs.order_by('username')
                elif sort_dir == 'DESC':
                    return qs.order_by('-username')
            elif sort_by == 'registered':
                if sort_dir == 'ASC':
                    return qs.order_by('date_joined')
                elif sort_dir == 'DESC':
                    return qs.order_by('-date_joined')
            elif sort_by == 'num_posts':
                if sort_dir == 'ASC':
                    return qs.order_by('forum_profile__post_count')
                elif sort_dir == 'DESC':
                    return qs.order_by('-forum_profile__post_count')
        else:
            return qs
