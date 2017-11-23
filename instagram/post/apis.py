from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from utils import permissions as custom_permissions


from post.models import Post, PostLike
from post.serializer import PostSerializer
from utils.pagination import PostPagination


class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        custom_permissions.IsAuthorOrReadOnly,
    )


class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user in instance.liked.all():
            liked = PostLike.objects.get(author_id=user.pk, post_id=instance.pk)
            liked.delete()

        else:
            PostLike.objects.create(author_id=user.pk, post_id=instance.pk)

        data = {
            'post': PostSerializer(instance).data
        }
        return Response(data)
