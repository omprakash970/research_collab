from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from apps.accounts.models import Profile


# ──────────────────────────────────────────────
# Authentication
# ──────────────────────────────────────────────

def login_view(request):
    """Display login form and authenticate the user via Django's AuthenticationForm."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('accounts:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log the user out and redirect to the login page."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


# ──────────────────────────────────────────────
# Role-based dashboard redirect
# ──────────────────────────────────────────────

@login_required
def dashboard_redirect(request):
    """Redirect the authenticated user to the correct role-based dashboard."""
    role = request.user.profile.role

    if role == Profile.Role.ADMIN:
        return redirect('accounts:admin_dashboard')
    return redirect('accounts:researcher_dashboard')


# ──────────────────────────────────────────────
# Dashboards
# ──────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    """Dashboard view for ADMIN users. Redirects non-admins with a warning."""
    if request.user.profile.role != Profile.Role.ADMIN:
        messages.warning(request, 'You do not have access to the admin dashboard.')
        return redirect('accounts:dashboard')
    return render(request, 'accounts/admin_dashboard.html')


@login_required
def researcher_dashboard(request):
    """Dashboard view for RESEARCHER users. Redirects non-researchers with a warning."""
    if request.user.profile.role != Profile.Role.RESEARCHER:
        messages.warning(request, 'You do not have access to the researcher dashboard.')
        return redirect('accounts:dashboard')
    return render(request, 'accounts/researcher_dashboard.html')

