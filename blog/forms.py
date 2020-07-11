from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget


class PostCreateForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget())
    published_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = ['title'
            , 'slug'
            , 'category'
            , 'description'
            , 'image'
            , 'published_date']

# toastr.info('Hi! I am info message.');