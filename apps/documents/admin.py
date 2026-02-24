from django.contrib import admin

from apps.documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'uploaded_by', 'filename', 'uploaded_at')
    list_filter = ('project', 'uploaded_at')
    search_fields = ('title', 'project__title', 'uploaded_by__username')
    readonly_fields = ('uploaded_at',)
    date_hierarchy = 'uploaded_at'

    @admin.display(description='File')
    def filename(self, obj):
        """Show just the filename in the admin list."""
        return obj.filename

