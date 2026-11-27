from django.contrib import admin

from .models import StudySession


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "started_at", "duration_min")
    list_filter = ("course", "started_at")
    date_hierarchy = "started_at"