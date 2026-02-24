from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.accounts.models import Profile


class ProfileInline(admin.StackedInline):
    """Inline Profile editor shown on the User change page."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    """Extend the default User admin to include the Profile inline."""
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')

    @admin.display(description='Role', ordering='profile__role')
    def get_role(self, obj):
        """Show the user's profile role in the admin list view."""
        try:
            return obj.profile.get_role_display()
        except Profile.DoesNotExist:
            return '—'


# Re-register User with our enhanced admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

