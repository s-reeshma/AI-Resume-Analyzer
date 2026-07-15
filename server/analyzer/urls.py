from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import upload_resume, check_task_status, signup, analysis_history

urlpatterns = [
    path("upload/", upload_resume),
    path("task-status/<str:task_id>/", check_task_status),
    path("auth/signup/", signup),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("history/", analysis_history),
]
