from django.urls import path

from apps.communication import views

app_name = 'communication'

urlpatterns = [
    path(
        'project/<int:project_id>/messages/',
        views.project_messages,
        name='project_messages',
    ),
]

