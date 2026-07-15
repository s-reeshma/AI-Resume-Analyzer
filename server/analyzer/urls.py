from django.urls import path
from .views import upload_resume, check_task_status

urlpatterns = [
    path("upload/", upload_resume),
    path("task-status/<str:task_id>/", check_task_status),
]