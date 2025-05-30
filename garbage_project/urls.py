from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django's built-in authentication urls: login/logout
    path('accounts/', include('django.contrib.auth.urls')),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Garbage app urls
    path('', include('garbage.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
