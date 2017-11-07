from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post
from post.serializer import PostSerializer


class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)