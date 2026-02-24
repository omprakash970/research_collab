from functools import wraps

from django.http import HttpResponseForbidden

from apps.accounts.models import Profile


def role_required(role):
    """Decorator that restricts a view to users with a specific profile role."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if request.user.profile.role != role:
                return HttpResponseForbidden(
                    '<h3 style="text-align:center;margin-top:60px;">'
                    '403 — You do not have permission to access this page.'
                    '</h3>'
                )
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def admin_required(view_func):
    """Shortcut decorator: only ADMIN users may access this view."""
    return role_required(Profile.Role.ADMIN)(view_func)

