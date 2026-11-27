from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("", include("dashboard.urls")),
    path("study/", include("study.urls")),
    path("assignments/", include("assignments.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
]