from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def api_root(request):
    return JsonResponse({
        "users": "/api/users/",
        "posts": "/api/posts/",
        "notifications": "/api/notifications/"
    })

urlpatterns = [
    path("admin/", admin.site.urls),

    # API root
    path("api/", api_root, name="api-root"),

    # Users endpoints
    path("api/users/", include("users.urls")),

    # Posts endpoints (includes posts and comments)
    path("api/posts/", include("posts.urls")),

    # Notifications endpoints
    path("api/notifications/", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
