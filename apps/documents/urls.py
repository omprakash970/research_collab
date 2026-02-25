from django.urls import path

from apps.documents import views

app_name = 'documents'

urlpatterns = [
    path('project/<int:project_id>/', views.document_list, name='document_list'),
    path('project/<int:project_id>/upload/', views.document_upload, name='document_upload'),
    path('project/<int:project_id>/delete/<int:document_id>/', views.document_delete, name='document_delete'),
]

