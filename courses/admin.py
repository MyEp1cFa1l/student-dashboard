from django.contrib import admin
from .models import Course, ScheduleSlot

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'semester', 'teacher')
    list_filter = ('semester', 'teacher')
    search_fields = ('title',)
    # Никаких форм, виджетов и медиа. Всё по стандарту.

@admin.register(ScheduleSlot)
class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time', 'end_time', 'course', 'format', 'classroom')
    list_filter = ('day_of_week', 'format', 'course')