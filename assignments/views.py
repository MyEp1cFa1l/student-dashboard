from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import AssignmentForm, AssignmentStatusForm, CommentForm
from .models import Assignment

class AssignmentGradeForm(forms.Form):
    grade = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Например, 85'})
    )
    max_grade = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, initial=100.00,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

@login_required
def assignment_list(request):
    """Страница со списком всех заданий."""
    # Берем ВСЕ задания пользователя (и сделанные, и нет) и сортируем по дате
    assignments = Assignment.objects.filter(
        course__user=request.user
    ).order_by('due_at')
    
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, course__user=request.user)
    
    if request.method == 'POST':
        # 1. Если нажали кнопку смены статуса (сработал onchange в селекте)
        if 'update_status' in request.POST:
            status_form = AssignmentStatusForm(request.POST, instance=assignment)
            if status_form.is_valid():
                updated_assignment = status_form.save(commit=False)
                
                # МАГИЯ: Если статус стал "Выполнено", но оценки нет - ставим максимум
                if updated_assignment.status == 'done' and updated_assignment.grade is None:
                    updated_assignment.grade = updated_assignment.max_grade
                    
                updated_assignment.save()
                return redirect('assignments:detail', pk=assignment.pk)
        
        # 2. Если отправили комментарий
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.assignment = assignment
                comment.author = request.user
                comment.save()
                return redirect('assignments:detail', pk=assignment.pk)
                
        # 3. Если обновили оценку
        elif 'update_grade' in request.POST:
            grade_form = AssignmentGradeForm(request.POST)
            if grade_form.is_valid():
                # Сохраняем вручную в объект assignment
                assignment.grade = grade_form.cleaned_data['grade']
                assignment.max_grade = grade_form.cleaned_data['max_grade']
                assignment.save()
                return redirect('assignments:detail', pk=assignment.pk)
                
    else:
        status_form = AssignmentStatusForm(instance=assignment)
        comment_form = CommentForm()
        # Передаем текущие значения оценок в форму
        grade_form = AssignmentGradeForm(initial={
            'grade': assignment.grade,
            'max_grade': assignment.max_grade
        })

    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment,
        'status_form': status_form,
        'comment_form': comment_form,
        'grade_form': grade_form, # <-- Передаем форму оценки
    })

@login_required
def assignment_add(request):
    """Добавление нового задания."""
    if request.method == 'POST':
        # Передаем user в форму, чтобы отфильтровать курсы
        form = AssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('assignments:list') # Перекидываем на список заданий
    else:
        form = AssignmentForm(user=request.user)
    
    return render(request, 'assignments/assignment_form.html', {'form': form})