from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import Profile
from apps.documents.forms import DocumentUploadForm
from apps.projects.models import ResearchProject


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _user_can_access_project(user, project):
    """Return True if the user is ADMIN or an assigned researcher."""
    if user.profile.role == Profile.Role.ADMIN:
        return True
    return user in project.researchers.all()


# ──────────────────────────────────────────────
# Document List
# ──────────────────────────────────────────────

@login_required
def document_list(request, project_id):
    """
    Show all documents for a project.
    ADMIN → can view any project's documents.
    RESEARCHER → can view only if assigned to the project.
    """
    project = get_object_or_404(ResearchProject, pk=project_id)

    if not _user_can_access_project(request.user, project):
        return HttpResponseForbidden(
            '<h3 style="text-align:center;margin-top:60px;">'
            '403 — You do not have permission to view these documents.'
            '</h3>'
        )

    documents = project.documents.select_related('uploaded_by').all()
    is_admin = request.user.profile.role == Profile.Role.ADMIN

    context = {
        'project': project,
        'documents': documents,
        'is_admin': is_admin,
    }
    return render(request, 'documents/document_list.html', context)


# ──────────────────────────────────────────────
# Document Upload
# ──────────────────────────────────────────────

@login_required
def document_upload(request, project_id):
    """
    Upload a document to a project.
    ADMIN → can upload to any project.
    RESEARCHER → can upload only to assigned projects.
    """
    project = get_object_or_404(ResearchProject, pk=project_id)

    if not _user_can_access_project(request.user, project):
        return HttpResponseForbidden(
            '<h3 style="text-align:center;margin-top:60px;">'
            '403 — You do not have permission to upload documents to this project.'
            '</h3>'
        )

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.project = project
            document.uploaded_by = request.user
            document.save()
            messages.success(request, f'Document "{document.title}" uploaded successfully.')
            return redirect('documents:document_list', project_id=project.pk)
    else:
        form = DocumentUploadForm()

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'documents/document_upload.html', context)

