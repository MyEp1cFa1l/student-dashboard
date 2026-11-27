from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path("", views.assignment_list, name="list"),
    path("add/", views.assignment_add, name="add"),
    path("<int:pk>/", views.assignment_detail, name="detail"),
]