from django import forms
from .models import Assignment, Comment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'due_at', 'weight', 'max_score', 'status']
        widgets = {
            'due_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            # добавь другие виджеты, если нужно
        }

    def __init__(self, *args, **kwargs):
        # Извлекаем пользователя, чтобы отфильтровать курсы
        user = kwargs.pop('user', None)
        super(AssignmentForm, self).__init__(*args, **kwargs)
        
        # Настройка формата для даты (как было у тебя)
        self.fields['due_at'].input_formats = ['%Y-%m-%dT%H:%M']
        
        if user is not None:
            self.fields['course'].queryset = self.fields['course'].queryset.filter(user=user)


class AssignmentStatusForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишите, как продвигается работа...'}),
        }