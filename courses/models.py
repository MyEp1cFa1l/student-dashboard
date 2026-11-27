from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    """Учебный курс (предмет)."""

    TAGS_CHOICES = [
        ('programming', 'Программирование'),
        ('math', 'Математика'),
        ('design', 'Дизайн и UI/UX'),
        ('management', 'Менеджмент и бизнес'),
        ('easy', 'Легкая аттестация'),
        ('hard', 'Хардкор и много практики'),
        ('gyman', 'Гуманитарная дисциплина'),
    ]

    tags = models.CharField(max_length=255, blank=True, verbose_name="Теги (критерии)")

    def get_tags_list(self):
        if self.tags:
            return self.tags.split(',')
        return []

    SEMESTER_CHOICES = [
        ("2025-Summer", "Лето 2025"),
        ("2026-Winter", "Зима 2026"),
        ("2026-Summer", "Лето 2026"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    title = models.CharField("Название", max_length=200)
    teacher = models.CharField("Преподаватель", max_length=200, blank=True)
    credits = models.PositiveSmallIntegerField("Кредиты", default=3)
    semester = models.CharField(
        "Семестр", max_length=20, choices=SEMESTER_CHOICES, default="2025-Fall"
    )
    color = models.CharField(
        "Цвет", max_length=7, default="#4f46e5",
        help_text="HEX-цвет, например #4f46e5",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        'assignments.Teacher', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Преподаватель"
    )
    is_archived = models.BooleanField(default=False, verbose_name="В архиве")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title

    @property
    def average_grade(self):
        # Берем все задания по этому курсу, у которых есть оценка (grade не пустой)
        graded = self.assignment_set.filter(grade__isnull=False)
        
        # Если таких заданий нет, возвращаем None
        if not graded.exists():
            return None
        
        # Считаем средний процент
        total = 0
        for a in graded:
            # Делим полученный балл на максимум и умножаем на 100
            percent = (float(a.grade) / float(a.max_grade)) * 100
            total += percent
            
        return round(total / graded.count(), 1)

    @property
    def has_ungraded_completed(self):
        return self.assignment_set.filter(status='done', grade__isnull=True).exists()

    @property
    def gpa_color(self):
        avg = self.average_grade
        if avg is None:
            return 'text-muted' # Серый, если оценок нет
        elif avg >= 80:
            return 'text-success' # Зеленый
        elif avg >= 50:
            return 'text-warning' # Желтый
        else:
            return 'text-danger' # Красный

class ScheduleSlot(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
    ]

    FORMAT_CHOICES = [
        ('offline', 'Офлайн (в аудитории)'),
        ('online', 'Онлайн (ссылка/Zoom)'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name="День недели")
    
    # Время начала и конца пары
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='offline', verbose_name="Формат")
    
    # Для офлайна - аудитория, для онлайна - ссылка
    classroom = models.CharField(max_length=50, blank=True, verbose_name="Аудитория (для офлайн)")
    online_link = models.URLField(blank=True, verbose_name="Ссылка (для онлайн)")

    class Meta:
        verbose_name = 'Занятие в расписании'
        verbose_name_plural = 'Расписание'
        # Сортировка: сначала по дням, потом по времени
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        # Красивое отображение в админке (например: "Понедельник 08:30 - Программирование")
        return f"{self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')} - {self.course.title}"

class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name="Курс")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка (1-5)"
    )
    text = models.TextField(verbose_name="Текст отзыва", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # Один пользователь может оставить только один отзыв на курс
        unique_together = ('course', 'user') 
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.course.title}"