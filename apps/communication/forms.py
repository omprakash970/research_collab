from django import forms

from apps.communication.models import ProjectMessage


class ProjectMessageForm(forms.ModelForm):
    """Form for posting a message to a project discussion thread."""

    class Meta:
        model = ProjectMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message…',
            }),
        }
        labels = {
            'message': '',
        }

