from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "users": reverse('user-list', request=request, format=format),
        "posts": reverse('post-list', request=request, format=format),
        "comments": reverse('comment-list', request=request, format=format),
        "notifications": reverse('notifications', request=request, format=format),
        "feed": reverse('user-feed', request=request, format=format),
    })
