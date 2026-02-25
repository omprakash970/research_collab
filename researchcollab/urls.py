"""
researchcollab – Root URL configuration.

All app-level URL modules are included here under their respective prefixes.
Media files are served by Django only when DEBUG is True.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from . import views as root_views

# ──────────────────────────────────────────────
# Admin site branding
# ──────────────────────────────────────────────
admin.site.site_header = 'ResearchCollab Administration'
admin.site.site_title = 'ResearchCollab Admin'
admin.site.index_title = 'Platform Management'

urlpatterns = [
    # Root URL → login page
    path('', lambda request: redirect('accounts:login'), name='home'),

    # Route map (lists all available pages)
    path('routes/', root_views.routes_view, name='routes'),

    path('admin/', admin.site.urls),

    # App URL includes
    path('', include('apps.accounts.urls')),
    path('projects/', include('apps.projects.urls')),
    path('documents/', include('apps.documents.urls')),
    path('communication/', include('apps.communication.urls')),
]

# Serve user-uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

