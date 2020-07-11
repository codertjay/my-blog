from django.contrib import messages
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType

from blog.models import Post
from .models import Comment
from .forms import CommentForm


def comment_thread(request,id=None):
    try:
        obj = Comment.objects.get(id=id)
    except:
        obj = None
    content_object = obj.content_object # this is another way to get content_object the from our comment model
    content_id = obj.content_object.id # this is another way to get object_id the from our comment model
    form = CommentForm(request.POST or None)
    context = {
        'object': obj,
        'form': form
    }
    form = CommentForm(request.POST or None)
    print(dir(form))
    print('content_type: ', obj.content_type)
    print('object_id: ', obj.object_id)

    if form.is_valid():
        print(form.cleaned_data)
        form_data = form.save(commit=False)
        form_data.user = request.user
        """
        we dont need to get the object id form our model we already have it 
        because in here are just creating a comment thread which is replying to our first comment
        so we just get the content_object and object_id from our form 
        """
        form_data.content_type = obj.content_type
        form_data.object_id = obj.object_id
        form_data.parent = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
                print('parent_obj :', parent_obj)
                form_data.parent = parent_obj
        form.save()
        messages.success(request, 'form has being submitted')
        """
        redirecting to the instance model get absolute url  which is the 
        detail page
        """
        return HttpResponseRedirect(form_data.content_object.get_absolute_url())

    return render(request, 'comments/comment_thread.html', context)


def comment_delete(request,id):
    try:
        obj = Comment.objects.get(id=id)
    except:
        response = HttpResponse("You do not have permission to delete this post")
        response.status_code = 403
        raise response
    context={
        'object':obj
    }
    if obj.user != request.user:
        raise Http404
    if request.method == 'POST':
        # parent_obj_url will be which is the post get_absolute_url()
        # or any app that will like to use this delete
        parent_obj_url = obj.content_object.get_absolute_url()

        if not obj.is_parent:
            obj = obj.parent
        if obj.user == request.user:
            obj.delete()
        messages.info(request,'the comment thread has being deleted')
        return HttpResponseRedirect(parent_obj_url)
    return render(request,'comments/comment_delete.html',context)




