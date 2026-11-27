from django import forms
from .models import StudySession

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['course', 'duration_min', 'note']
        widgets = {
            'course': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm p-2'}),
            'duration_min': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm p-2'}),
            'note': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm p-2', 'placeholder': 'Что изучали?'}),
        }