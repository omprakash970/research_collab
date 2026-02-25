"""
Root-level views for the researchcollab project.
"""
from django.shortcuts import render


def routes_view(request):
    """Display a page listing all available routes in the application."""
    routes = [
        {
            'section': 'Authentication',
            'items': [
                {'name': 'Login', 'url': '/login/', 'method': 'GET / POST', 'description': 'Sign in to your account'},
                {'name': 'Logout', 'url': '/logout/', 'method': 'GET', 'description': 'Sign out of your account'},
                {'name': 'Register', 'url': '/register/', 'method': 'GET / POST', 'description': 'Create a new account'},
                {'name': 'Change Password', 'url': '/password/change/', 'method': 'GET / POST', 'description': 'Change your current password'},
                {'name': 'Change Password Done', 'url': '/password/change/done/', 'method': 'GET', 'description': 'Password change confirmation'},
                {'name': 'Set Password', 'url': '/password/set/', 'method': 'GET / POST', 'description': 'Set a password (if none exists)'},
            ],
        },
        {
            'section': 'Dashboards',
            'items': [
                {'name': 'Dashboard (redirect)', 'url': '/dashboard/', 'method': 'GET', 'description': 'Redirects to role-based dashboard'},
                {'name': 'Admin Dashboard', 'url': '/dashboard/admin/', 'method': 'GET', 'description': 'Dashboard for ADMIN users'},
                {'name': 'Researcher Dashboard', 'url': '/dashboard/researcher/', 'method': 'GET', 'description': 'Dashboard for RESEARCHER users'},
            ],
        },
        {
            'section': 'Projects',
            'items': [
                {'name': 'Project List', 'url': '/projects/', 'method': 'GET', 'description': 'List all projects (role-filtered)'},
                {'name': 'Create Project', 'url': '/projects/create/', 'method': 'GET / POST', 'description': 'Create a new project (ADMIN only)'},
                {'name': 'Project Detail', 'url': '/projects/<id>/', 'method': 'GET', 'description': 'View project details'},
                {'name': 'Edit Project', 'url': '/projects/<id>/edit/', 'method': 'GET / POST', 'description': 'Edit a project (ADMIN only)'},
            ],
        },
        {
            'section': 'Documents',
            'items': [
                {'name': 'Document List', 'url': '/documents/project/<project_id>/', 'method': 'GET', 'description': 'List documents for a project'},
                {'name': 'Upload Document', 'url': '/documents/project/<project_id>/upload/', 'method': 'GET / POST', 'description': 'Upload a document to a project'},
                {'name': 'Delete Document', 'url': '/documents/project/<project_id>/delete/<document_id>/', 'method': 'GET / POST', 'description': 'Delete a document (uploader or ADMIN)'},
            ],
        },
        {
            'section': 'Communication',
            'items': [
                {'name': 'Project Messages', 'url': '/communication/project/<project_id>/messages/', 'method': 'GET / POST', 'description': 'View and post messages for a project'},
            ],
        },
        {
            'section': 'Admin',
            'items': [
                {'name': 'Django Admin Panel', 'url': '/admin/', 'method': 'GET', 'description': 'Django administration interface'},
            ],
        },
    ]

    return render(request, 'routes.html', {'routes': routes})

