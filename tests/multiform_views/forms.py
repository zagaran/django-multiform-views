from django import forms

from .models import Journalist


class JournalistForm(forms.ModelForm):
    name = forms.CharField()
    slug = forms.SlugField()
    email = forms.EmailField()

    class Meta:
        model = Journalist
        fields = ['name', 'slug', 'email']


class CommentForm(forms.Form):
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)