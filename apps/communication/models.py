from django.contrib.auth.models import User
from django.db import models

from apps.projects.models import ResearchProject


class ProjectMessage(models.Model):
    project = models.ForeignKey(
        ResearchProject,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Project Message'
        verbose_name_plural = 'Project Messages'

    def __str__(self):
        return f'{self.sender.username} → {self.project.title} ({self.created_at:%Y-%m-%d %H:%M})'

