from django.conf import settings
from django.db import models

from courses.models import Course


class StudySession(models.Model):
    """Сессия учёбы (запись таймера)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="study_sessions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="study_sessions",
    )
    started_at = models.DateTimeField("Начало")
    duration_min = models.PositiveIntegerField("Длительность, мин")
    note = models.CharField("Заметка", max_length=300, blank=True)

    class Meta:
        ordering = ["-started_at"]
        verbose_name = "Сессия учёбы"
        verbose_name_plural = "Сессии учёбы"

    def __str__(self):
        return f"{self.started_at:%Y-%m-%d} — {self.duration_min} мин"