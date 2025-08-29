from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users endpoints
    path('api/users/', include('users.urls')),

    # Posts endpoints (includes posts and comments)
    path('api/posts/', include('posts.urls')),

    # Notifications endpoints
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
