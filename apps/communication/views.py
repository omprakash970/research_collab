from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import Profile
from apps.communication.forms import ProjectMessageForm
from apps.communication.models import ProjectMessage
from apps.projects.models import ResearchProject


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _user_can_access_project(user, project):
    """Return True if the user is ADMIN or an assigned researcher."""
    if user.profile.role == Profile.Role.ADMIN:
        return True
    return user in project.researchers.all()


def _forbidden_response(msg='You do not have permission to access this discussion.'):
    return HttpResponseForbidden(
        f'<h3 style="text-align:center;margin-top:60px;">403 — {msg}</h3>'
    )


# ──────────────────────────────────────────────
# Project Messages  (GET thread + POST new msg)
# ──────────────────────────────────────────────

@login_required
def project_messages(request, project_id):
    """
    Display the message thread for a project and handle new message posts.
    ADMIN → can access any project's discussion.
    RESEARCHER → can access only if assigned to the project.
    """
    project = get_object_or_404(ResearchProject, pk=project_id)

    if not _user_can_access_project(request.user, project):
        return _forbidden_response()

    # Handle new message submission
    if request.method == 'POST':
        form = ProjectMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.project = project
            msg.sender = request.user
            msg.save()
            return redirect('communication:project_messages', project_id=project.pk)
    else:
        form = ProjectMessageForm()

    thread = project.messages.select_related('sender').all()

    context = {
        'project': project,
        'thread': thread,
        'form': form,
        'is_admin': request.user.profile.role == Profile.Role.ADMIN,
    }
    return render(request, 'communication/project_messages.html', context)

