from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),
    path("add/", views.course_add, name="add"),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('recommend/', views.course_recommendation, name='recommend'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('course/<int:course_id>/reviews/', views.course_reviews, name='reviews'),
    path('course/<int:course_id>/toggle-archive/', views.toggle_archive, name='toggle_archive'),
    path('profile/', views.profile_view, name='profile'),
]