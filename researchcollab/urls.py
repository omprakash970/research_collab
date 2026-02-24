"""
researchcollab – Root URL configuration.

All app-level URL modules are included here under their respective prefixes.
Media files are served by Django only when DEBUG is True.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# ──────────────────────────────────────────────
# Admin site branding
# ──────────────────────────────────────────────
admin.site.site_header = 'ResearchCollab Administration'
admin.site.site_title = 'ResearchCollab Admin'
admin.site.index_title = 'Platform Management'

urlpatterns = [
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

