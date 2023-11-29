# study_groups/forms.py

from django import forms
from .models import StudyGroup, Message


class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
