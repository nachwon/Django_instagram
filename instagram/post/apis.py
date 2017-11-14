from rest_framework import generics, mixins, permissions
from utils import permissions as custom_permissions


from post.models import Post
from post.serializer import PostSerializer


class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
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
    def post(self, request, *args, **kwargs):
        instance = self.get_object()