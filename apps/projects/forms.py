from django import forms
from django.contrib.auth.models import User

from apps.accounts.models import Profile
from apps.projects.models import ResearchProject


class ResearchProjectForm(forms.ModelForm):
    """Form for creating and editing research projects (ADMIN only)."""

    researchers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role=Profile.Role.RESEARCHER),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Researchers',
    )

    class Meta:
        model = ResearchProject
        fields = ['title', 'description', 'status', 'researchers']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the research project…',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

