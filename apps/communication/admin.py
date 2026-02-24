from django.contrib import admin

from apps.communication.models import ProjectMessage


@admin.register(ProjectMessage)
class ProjectMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'project', 'short_message', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('message', 'sender__username', 'project__title')
    readonly_fields = ('created_at',)

    @admin.display(description='Message')
    def short_message(self, obj):
        """Truncate long messages in the admin list view."""
        if len(obj.message) > 80:
            return obj.message[:80] + '…'
        return obj.message

