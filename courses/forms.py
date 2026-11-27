from django import forms
from .models import Course, CourseReview
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    # Явно объявляем поле tags, чтобы Django точно знал его варианты
    tags = forms.MultipleChoiceField(
        choices=Course.TAGS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Критерии курса"
    )

    class Meta:
        model = Course
        # Явно перечисляем нужные поля. Убираем 'user'!
        fields = ['title', 'credits', 'semester', 'color', 'teacher', 'tags']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            # Поле semester лучше сделать выпадающим списком, если в модели есть choices
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем галочки, если редактируем существующий курс
        if self.instance and self.instance.pk and self.instance.tags:
            self.initial['tags'] = self.instance.tags.split(',')

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            return ",".join(tags)
        return ""

class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} звезд") for i in range(5, 0, -1)], attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Поделитесь впечатлениями о курсе...'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email') # Оставляем только это
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap для красоты
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Убираем ссылку на смену пароля отсюда, чтобы не путать пользователя
        if 'password' in self.fields:
            del self.fields['password']