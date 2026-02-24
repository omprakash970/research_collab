from django.urls import path

from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Password management
    path('password/change/', views.password_change_view, name='password_change'),
    path('password/change/done/', views.password_change_done_view, name='password_change_done'),
    path('password/set/', views.password_set_view, name='password_set'),

    # Dashboards
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/researcher/', views.researcher_dashboard, name='researcher_dashboard'),
]

