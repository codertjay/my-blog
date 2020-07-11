from django.shortcuts import render, redirect
from .forms import UserRegisterForm

from blog.models import Post


def home(request):
    post = Post.objects.published()[:3]
    context = {
        'posts': post
    }
    return render(request,'home-page.html',context)


