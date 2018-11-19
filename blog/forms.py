from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from blog.models import BlogPost
from blog.utils import generate_slug, clean_value, allow_clean_links


class BlogPostForm(forms.ModelForm):
    """
    ModelForm to validate and save BlogPosts.
    """
    def clean_title(self):
        is_add = self.instance.pk is None
        # if a blog already exists with a similar title or
        # with a slug similar to one generated from the title,
        # raise error to notify the user about the same.
        self.slug = generate_slug(self.cleaned_data['title'])
        query = BlogPost.objects.filter(Q(title=self.cleaned_data['title']) | Q(slug=self.slug))
        if is_add:
            # during add.
            if query.count() > 0:
                raise forms.ValidationError(_('Blog with a similar title already exists.'))
        else:
            # during edit.
            if query.exclude(pk=self.instance.pk).count() > 0:
                raise forms.ValidationError(_('Blog with a similar title already exists.'))

        # make sure title is alphanumeric.
        try:
            int(self.cleaned_data['title'])
        except ValueError as e:
            pass
        else:
            raise forms.ValidationError(_('Invalid value.'))

        return clean_value(self.cleaned_data['title'], tags=[])  # remove all HTML tags.

    def clean_description(self):
        # make sure it is alphanumeric.
        try:
            int(self.cleaned_data['description'])
        except ValueError as e:
            pass
        else:
            raise forms.ValidationError(_('Invalid value.'))

        return clean_value(
            self.cleaned_data['description'],
            attrs={
                'a': allow_clean_links,  # allow anchor tags which has no javascripts.
                'abbr': ['title'],
                'acronym': ['title'],
                'pre': []
            }
        )  # remove malicious HTML tags.

    class Meta:
        model = BlogPost
        exclude = ['slug']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
