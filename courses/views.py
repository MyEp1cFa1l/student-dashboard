from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Course, ScheduleSlot, CourseReview
from .forms import CourseForm, CourseReviewForm
from assignments.models import Teacher 
from .forms import CustomUserChangeForm
from django.contrib import messages

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'courses/teacher_list.html', {'teachers': teachers})

@login_required
def course_list(request):
    # Берем ВСЕ курсы пользователя
    all_courses = Course.objects.filter(user=request.user)
    
    # Разделяем их на активные и архивные
    active_courses = all_courses.filter(is_archived=False)
    archived_courses = all_courses.filter(is_archived=True)
    
    return render(request, "courses/course_list.html", {
        "active_courses": active_courses,
        "archived_courses": archived_courses
    })

@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # commit=False позволяет не сохранять объект в БД прямо сейчас
            course = form.save(commit=False)
            # Привязываем курс к текущему пользователю
            course.user = request.user 
            # Теперь сохраняем в базу
            course.save()
            # После сохранения возвращаем к списку курсов
            return redirect('courses:list') 
    else:
        # Если это GET-запрос (пользователь просто открыл страницу), создаем пустую форму
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def course_recommendation(request):
    """Страница опросника для подбора курсов."""
    recommended_courses = None
    
    if request.method == 'POST':
        # Получаем список выбранных чекбоксов (например, ['math', 'programming'])
        selected_tags = request.POST.getlist('tags')
        
        # Если пользователь что-то выбрал
        if selected_tags:
            # Мы будем искать курсы, в поле tags которых есть хотя бы один из выбранных критериев
            query = Q()
            for tag in selected_tags:
                # tags__icontains ищет подстроку (например, 'math' найдет 'programming,math')
                query |= Q(tags__icontains=tag)
                
            # distinct() нужен, чтобы один и тот же курс не вывелся дважды, 
            # если он подошел по двум критериям
            recommended_courses = Course.objects.filter(query).distinct()
    
    # Передаем список тегов для отображения чекбоксов в шаблоне
    context = {
        'tags_choices': Course.TAGS_CHOICES,
        'recommended_courses': recommended_courses,
        # Сохраняем выбранные теги, чтобы галочки не сбрасывались после отправки формы
        'selected_tags': request.POST.getlist('tags') if request.method == 'POST' else []
    }
    
    return render(request, 'courses/course_recommendation.html', context)

@login_required
def schedule_view(request):
    slots = ScheduleSlot.objects.filter(course__user=request.user)
    
    # Создаем список дней недели с занятиями внутри
    days_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота',]
    
    # Создаем список словарей
    schedule_data = []
    for i, day_name in enumerate(days_names):
        # Находим все занятия для текущего дня (i - это индекс от 0 до 6)
        day_slots = [slot for slot in slots if slot.day_of_week == i]
        schedule_data.append({
            'day_name': day_name,
            'slots': day_slots
        })

    context = {
        'schedule_data': schedule_data,
    }
    return render(request, 'courses/schedule.html', context)

@login_required
def course_reviews(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = course.reviews.all()
    
    # Проверяем, может ли текущий пользователь оставить отзыв
    # (Есть ли у него выполненные задания по этому курсу)
    has_completed_tasks = Assignment.objects.filter(course=course, status='done').exists()
    # Проверяем, не оставлял ли он уже отзыв
    user_has_reviewed = CourseReview.objects.filter(course=course, user=request.user).exists()

    if request.method == 'POST' and has_completed_tasks and not user_has_reviewed:
        form = CourseReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('courses:reviews', course_id=course.id)
    else:
        form = CourseReviewForm()

    context = {
        'course': course,
        'reviews': reviews,
        'form': form,
        'has_completed_tasks': has_completed_tasks,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'courses/course_reviews.html', context)

@login_required
def toggle_archive(request, course_id):
    course = get_object_or_404(Course, id=course_id, user=request.user)
    # Меняем статус на противоположный
    course.is_archived = not course.is_archived
    course.save()
    return redirect('courses:list')

# --- НОВАЯ ВЬЮХА ДЛЯ ПРОФИЛЯ ---
@login_required
def profile_view(request):
    # 1. Обработка формы (если пользователь нажал "Сохранить")
    if request.method == 'POST':
        # Мы используем встроенную форму, но ограничиваем поля (чтобы нельзя было стать суперюзером)
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('courses:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    # 2. Сбор статистики для профиля
    all_courses = Course.objects.filter(user=request.user)
    
    # Считаем пройденные (архивные) курсы
    completed_courses_count = all_courses.filter(is_archived=True).count()
    active_courses_count = all_courses.filter(is_archived=False).count()

    # Считаем общий GPA по всем оцененным заданиям
    from assignments.models import Assignment
    graded_assignments = Assignment.objects.filter(course__user=request.user, grade__isnull=False)
    
    gpa = 0
    if graded_assignments.exists():
        total_percent = 0
        for a in graded_assignments:
            percent = (float(a.grade) / float(a.max_grade)) * 100
            total_percent += percent
        gpa = round(total_percent / graded_assignments.count(), 1)

    context = {
        'form': form,
        'completed_courses': completed_courses_count,
        'active_courses': active_courses_count,
        'gpa': gpa,
    }
    return render(request, 'courses/profile.html', context)