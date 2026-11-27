from django.conf import settings
from django.db import models
from django.utils import timezone

from courses.models import Course


class Assignment(models.Model):
    """Задание внутри курса (домашка, проект, экзамен)."""

    TYPE_CHOICES = [
        ("hw", "Домашнее задание"),
        ("kt", "Контрольная точка"),
        ("project", "Проект"),
        ("exam", "Экзамен"),
        ("wop", "Задание на паре"),
        ("other", "Другое"),
    ]
    STATUS_CHOICES = [
        ("todo", "Не начато"),
        ("doing", "В процессе"),
        ("done", "Сделано"),
    ]

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)

    title = models.CharField("Название", max_length=200)
    type = models.CharField(
        "Тип", max_length=10, choices=TYPE_CHOICES, default="hw"
    )
    due_at = models.DateTimeField("Дедлайн")
    weight = models.DecimalField(
        "Вес в оценке, %", max_digits=5, decimal_places=2, default=10
    )
    max_score = models.DecimalField(
        "Макс. балл", max_digits=6, decimal_places=2, default=100
    )
    status = models.CharField(
        "Статус", max_length=10, choices=STATUS_CHOICES, default="todo"
    )
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, verbose_name="Описание / Условие задачи")
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Полученный балл")
    max_grade = models.DecimalField(max_digits=5, decimal_places=2, default=100.00, verbose_name="Максимальный балл")

    class Meta:
        ordering = ["due_at"]
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return f"{self.course.title} — {self.title}"

    @property
    def is_overdue(self):
        return self.status != "done" and self.due_at < timezone.now()


class Grade(models.Model):
    """Оценка за задание."""

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grade_entries')
    score = models.DecimalField("Балл", max_digits=6, decimal_places=2)
    graded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выставления")
    comment = models.CharField("Комментарий", max_length=300, blank=True)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.assignment}: {self.score}/{self.assignment.max_score}"

    @property
    def percent(self):
        if self.assignment.max_score == 0:
            return 0
        return float(self.score) / float(self.assignment.max_score) * 100


class Comment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.assignment.title}"

class Teacher(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    department = models.CharField(max_length=200, verbose_name="Кафедра", blank=True)
    bio = models.TextField(verbose_name="О преподавателе", blank=True)
    # Если захочешь добавить фото, позже можно добавить ImageField

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return self.full_name