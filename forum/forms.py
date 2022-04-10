from django import forms

from forum.core.conf import settings
from forum.core.utils import set_language
from forum.models import Profile

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
