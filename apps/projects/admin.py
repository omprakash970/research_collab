from django.contrib import admin

from apps.projects.models import ResearchProject


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    filter_horizontal = ('researchers',)
    readonly_fields = ('created_at',)

