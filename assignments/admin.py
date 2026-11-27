from django.contrib import admin
from .models import Assignment, Teacher, Comment, Grade 

class GradeInline(admin.StackedInline):
    model = Grade
    extra = 0
    max_num = 1

class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ("title", "type", "due_at", "weight", "max_score", "status")
    show_change_link = True

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title", "course", "type", "due_at", "status", "weight", "max_score",
    )
    list_filter = ("type", "status", "course")
    search_fields = ("title", "course__title")
    date_hierarchy = "due_at"
    inlines = [GradeInline]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department')
    search_fields = ('full_name', 'department')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("assignment", "score", "graded_at")
    list_filter = ("graded_at",)
