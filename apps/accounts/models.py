from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        RESEARCHER = 'RESEARCHER', 'Researcher'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESEARCHER)

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'

