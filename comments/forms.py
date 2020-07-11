from django import forms
from .models import Comment



class CommentForm(forms.ModelForm):
    content = forms.CharField(label='',widget=forms.Textarea )
    class Meta:
        model = Comment
        fields = ['content']

