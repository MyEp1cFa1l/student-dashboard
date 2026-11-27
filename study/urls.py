from django.urls import path
from . import views

app_name = "study"

urlpatterns = [
    path("timer/", views.timer_view, name="timer"),
]