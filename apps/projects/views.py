from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import Profile
from apps.projects.decorators import admin_required
from apps.projects.forms import ResearchProjectForm
from apps.projects.models import ResearchProject


# ──────────────────────────────────────────────
# Project List
# ──────────────────────────────────────────────

@login_required
def project_list(request):
    """
    ADMIN  → sees every project.
    RESEARCHER → sees only projects they are assigned to.
    """
    role = request.user.profile.role

    if role == Profile.Role.ADMIN:
        projects = ResearchProject.objects.all()
    else:
        projects = request.user.assigned_projects.all()

    context = {
        'projects': projects,
        'is_admin': role == Profile.Role.ADMIN,
    }
    return render(request, 'projects/project_list.html', context)


# ──────────────────────────────────────────────
# Project Create  (ADMIN only)
# ──────────────────────────────────────────────

@login_required
@admin_required
def project_create(request):
    """Allow an ADMIN to create a new research project."""
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()  # save ManyToMany (researchers)
            messages.success(request, f'Project "{project.title}" created successfully.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ResearchProjectForm()

    return render(request, 'projects/project_create.html', {'form': form})


# ──────────────────────────────────────────────
# Project Detail
# ──────────────────────────────────────────────

@login_required
def project_detail(request, pk):
    """
    ADMIN → can view any project.
    RESEARCHER → can view only if assigned to the project.
    """
    project = get_object_or_404(ResearchProject, pk=pk)
    role = request.user.profile.role

    if role != Profile.Role.ADMIN and request.user not in project.researchers.all():
        return HttpResponseForbidden(
            '<h3 style="text-align:center;margin-top:60px;">'
            '403 — You do not have permission to view this project.'
            '</h3>'
        )

    context = {
        'project': project,
        'is_admin': role == Profile.Role.ADMIN,
    }
    return render(request, 'projects/project_detail.html', context)


# ──────────────────────────────────────────────
# Project Edit  (ADMIN only)
# ──────────────────────────────────────────────

@login_required
@admin_required
def project_edit(request, pk):
    """Allow an ADMIN to edit an existing research project."""
    project = get_object_or_404(ResearchProject, pk=pk)

    if request.method == 'POST':
        form = ResearchProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project "{project.title}" updated successfully.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ResearchProjectForm(instance=project)

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'projects/project_edit.html', context)

