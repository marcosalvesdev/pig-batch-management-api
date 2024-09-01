from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("batches_app.urls", namespace="batches_app")),
    path("admin/", admin.site.urls),
]
