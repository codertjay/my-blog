from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)

from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

from .permissions import IsOwnerOrReadonly
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

from blog.models import Post
from .serializers import (
    PostListSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer)


class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.published()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class PostDeleteApiView(DestroyAPIView):
    queryset = Post.objects.published()
    serializer_class = PostListSerializer
    permission_classes = [IsOwnerOrReadonly]
    lookup_field = 'slug'

    # def perform_destroy(self,serializer):
    #     serializer.delete(user=self.request.user)



class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.published()
    serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        """ this is to add the user that is creating the post
         to the post """
        serializer.save(user=self.request.user)


class PostListApiView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','slug','description']
    #  i created this pagination using the PageNumberPagination which
    # i imported from django with just a class
    pagination_class = PostPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        """ the reason why i comment this is because if there is a
        queryset then we in the class then we are going to use it
        but there is none so i am passing hte queryset in here """
        # query_list = super(PostListApiView,self).get_queryset(*args)
        post = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = post.filter(
                Q(category__icontains=query) |
                Q(description__icontains=query) |
                Q(user__username__icontains=query) |
                Q(title__icontains=query)
            ).distinct()
        else:
            query_list = Post.objects.all()
        return query_list


class PostUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.published()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadonly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


"""
obj = Post.objects.get(id=5)

data =   {
        "id": 6,
        "title": "Is it gonnna work",
        "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. A, accusantium ad, adipisci aliquam aliquid architecto aspernatur assumenda beatae, culpa eos esse explicabo labore libero magni maxime nam natus nemo neque nostrum odit officiis omnis quia quisquam quos reiciendis sapiente sed similique. Accusamus alias animi atque culpa delectus dicta, eius eligendi eos et eum facere id illo magni maiores nisi non numquam quaerat quos recusandae repudiandae sed sequi, tempore tenetur totam veniam! Aspernatur autem commodi dignissimos doloremque ducimus enim facere fugiat fugit neque numquam praesentium quasi quidem reprehenderit, rerum sapiente tempora voluptatum! Architecto doloremque harum similique. Corporis doloremque incidunt nulla perspiciatis repellat sit? Amet animi atque corporis delectus distinctio dolores dolorum eaque earum eius eligendi et facere, fugit hic id ipsam iusto labore magnam minus molestiae nisi nobis obcaecati possimus provident quae quam quasi quod reprehenderit rerum sint, sit suscipit tempora, velit voluptatum? Ab aperiam asperiores aut consequuntur debitis dolores ducimus eius, eos est eveniet ex exercitationem harum impedit itaque laboriosam magni molestiae natus nemo optio pariatur, placeat porro possimus quasi qui quibusdam quisquam, rem repellat similique sunt vitae. Accusamus architecto at debitis delectus ducimus in, libero, maxime minus non obcaecati omnis placeat saepe, tempore temporibus veniam vero voluptatem! Aliquam culpa cumque et iure minima. Ab cum, debitis hic id inventore laudantium modi molestias nam, nemo neque ratione totam unde velit? Beatae doloremque neque officia placeat voluptatum. Aliquam animi beatae culpa cumque delectus dolor dolorem ex nesciunt nihil pariatur, praesentium quas quo quos rerum sed! Exercitationem fuga, modi? A aspernatur cumque, dignissimos dolor, dolore dolores, earum laborum minima nobis nostrum quae sit soluta suscipit? Accusamus corporis cumque debitis dicta doloribus ducimus eaque nisi reiciendis, rem repudiandae! A aspernatur cupiditate dignissimos dolor doloremque eaque eligendi esse, exercitationem facilis iste laborum magnam, modi natus odio optio placeat provident quae quas quisquam reprehenderit repudiandae sit totam vero! Accusamus doloribus eius esse exercitationem explicabo, in ipsa ipsam iure labore libero maiores, maxime nam necessitatibus nisi officiis pariatur quae! Accusamus, aperiam aspernatur atque autem beatae debitis deleniti dicta dignissimos dolores ea enim eos eum eveniet excepturi facere fugit harum, illo labore laudantium magnam molestias nam nemo nihil nobis non obcaecati perferendis placeat quam quas quis ratione repellat reprehenderit similique totam voluptas voluptates voluptatum. Alias animi, atque, cum dolores ea earum eligendi eos esse fugiat harum labore, minus similique unde? Adipisci aliquid at delectus deserunt doloremque eligendi esse, illum itaque libero nam possimus provident recusandae, saepe sed tempora veniam voluptates. Accusantium cumque eum fugiat, laudantium nam pariatur quas quidem vel veniam? Ad adipisci, architecto asperiores autem consectetur doloremque inventore itaque labore non nulla quisquam recusandae sequi voluptatem. Accusamus accusantium architecto assumenda cumque dicta ducimus ea eius eveniet in ipsum iste itaque libero molestias natus officiis provident quaerat quas quisquam quo rerum, sapiente soluta temporibus tenetur ut veritatis? Ab ad aliquid architecto consectetur distinctio dolorem eaque hic ipsa iure, iusto maiores modi, nemo nobis non sequi unde ut, vitae. Aliquam atque aut blanditiis commodi debitis dignissimos, dolor, eaque et explicabo itaque, libero nobis repudiandae rerum sint vero! Corporis!",
        "category": "L",
        "timestamp": "2020-06-03T09:30:24.430944Z"
    },
new_item = PostDetailSerializer(obj,data=data)
if new_item.is_valid():
    new.save()
else:
    print(new_item.errors)

"""
