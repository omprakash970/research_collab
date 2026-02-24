from django import forms

from apps.documents.models import Document


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading a document to a research project."""

    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document title',
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

