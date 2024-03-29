from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls', namespace='about')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('posts.urls', namespace='posts')),
]

handler403 = 'core.views.permission_denied_view'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.internal_server_error_view'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
    )
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
