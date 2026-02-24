from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.shortcuts import redirect, render

from apps.accounts.forms import RegistrationForm
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
# Registration
# ──────────────────────────────────────────────

def register_view(request):
    """
    Register a new user account.

    The Profile (with default role RESEARCHER) is auto-created by the
    post_save signal — no role field is exposed on the form.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Account created successfully! You can now sign in.',
            )
            return redirect('accounts:login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ──────────────────────────────────────────────
# Password Management
# ──────────────────────────────────────────────

@login_required
def password_change_view(request):
    """Allow authenticated users to change their password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('accounts:password_change_done')
    else:
        form = PasswordChangeForm(request.user)

    # Apply Bootstrap classes to all fields
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control form-control-lg'})

    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def password_change_done_view(request):
    """Confirmation page shown after a successful password change."""
    return render(request, 'accounts/password_change_done.html')


@login_required
def password_set_view(request):
    """
    Allow users without a usable password to set one.

    This covers edge cases such as accounts created via the admin
    panel without a password or future social-auth integrations.
    """
    if request.user.has_usable_password():
        messages.info(request, 'You already have a password. Use "Change Password" instead.')
        return redirect('accounts:password_change')

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been set successfully.')
            return redirect('accounts:dashboard')
    else:
        form = SetPasswordForm(request.user)

    # Apply Bootstrap classes to all fields
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control form-control-lg'})

    return render(request, 'accounts/password_set.html', {'form': form})


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

