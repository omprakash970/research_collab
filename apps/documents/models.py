from django.contrib.auth.models import User
from django.db import models

from apps.projects.models import ResearchProject


class Document(models.Model):
    project = models.ForeignKey(
        ResearchProject,
        on_delete=models.CASCADE,
        related_name='documents',
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_documents',
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='project_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.title

    @property
    def filename(self):
        """Return just the file name from the full path."""
        return self.file.name.split('/')[-1]

