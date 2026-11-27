from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from courses.models import Course
from assignments.models import Assignment
from study.models import StudySession


@login_required
def index(request):
    user_courses = Course.objects.filter(user=request.user)
    
    # Считаем виджеты
    total_courses = user_courses.count()
    active_assignments = Assignment.objects.filter(
        course__user=request.user
    ).exclude(status='done').count()
    
    nearest_deadline = Assignment.objects.filter(
        course__user=request.user,
        due_at__gte=timezone.now()
    ).exclude(status='done').order_by('due_at').first()
    
    # Считаем общий GPA (среднее из средних по курсам)
    total_score = 0
    courses_with_grades = 0
    for course in user_courses:
        avg = course.average_grade
        if avg is not None:
            total_score += avg
            courses_with_grades += 1
            
    overall_gpa = round(total_score / courses_with_grades, 1) if courses_with_grades > 0 else 0

    # Данные для графика (время учебы по курсам)
    time_by_course = StudySession.objects.filter(
        user=request.user,
        course__isnull=False
    ).values('course__title').annotate(total_minutes=Sum('duration_min')).order_by('-total_minutes')
    
    chart_labels = [item['course__title'] for item in time_by_course]
    chart_data = [item['total_minutes'] for item in time_by_course]

    context = {
        'total_courses': total_courses,
        'active_assignments': active_assignments,
        'nearest_deadline': nearest_deadline,
        'overall_gpa': overall_gpa,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, "dashboard/index.html", context)