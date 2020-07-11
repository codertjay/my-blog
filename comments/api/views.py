from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)

from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)
from rest_framework.mixins import DestroyModelMixin
#  my own
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
)
from comments.models import Comment
from blog.api.permissions import IsOwnerOrReadonly
from blog.api.pagination import (
    PostLimitOffsetPagination,
    PostPageNumberPagination
)



class CommentCreateApiView(CreateAPIView):
    """ this si not doing all the comment s it is only doing the
     parent comment because we override it in our comment manager """
    queryset = Comment.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly ]

    """ i am using the serializer class i created on the serializer"""
    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        slug = self.request.GET.get('slug')
        parent_id = self.request.GET.get('parent_id',None)
        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )



class CommentListApiView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['user__username','content','user_first_name']
    """ i created this pagination using the PageNumberPagination which 
    i imported from django with just a class  """
    pagination_class = PostPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        """ the reason why i comment this is because if there is a
        queryset then we in the class then we are going to use it
        but there is none so i am passing hte queryset in here """
        # query_list = super(PostListApiView,self).get_queryset(*args)
        comment = Comment.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = comment.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)
            ).distinct()
        else:
            query_list = Comment.objects.all()
        return query_list


class CommentDetailAPIView(DestroyModelMixin,RetrieveUpdateAPIView):
    """ this is going to filter base on the id and all the comment
    because in our miodel manager we change all """
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadonly]
    lookup_field = 'id'

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)




