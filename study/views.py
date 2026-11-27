from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudySessionForm
from django.utils import timezone

@login_required
def timer_view(request):
    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.started_at = timezone.now() # Записываем текущее время
            session.save()
            return redirect('dashboard:index') # Возвращаем на главную после сохранения
    else:
        form = StudySessionForm()
    
    # Ограничиваем выбор курсов только текущим пользователем
    form.fields['course'].queryset = request.user.courses.all()
    
    return render(request, "study/timer.html", {"form": form})