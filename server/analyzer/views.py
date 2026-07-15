import os
import uuid
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, parser_classes, permission_classes, throttle_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework import status
from django.conf import settings
from celery.result import AsyncResult

from .tasks import analyze_resume_task
from .models import ResumeAnalysis
from .serializers import SignupSerializer, ResumeAnalysisSerializer


class UploadRateThrottle(SimpleRateThrottle):
    scope = "upload"

    def get_rate(self):
        return getattr(settings, "RESUME_UPLOAD_RATE", "10/hour")

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)  # client IP
        return self.cache_format % {"scope": self.scope, "ident": ident}


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Account created."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([AllowAny])
@throttle_classes([UploadRateThrottle])
def upload_resume(request):
    file = request.FILES.get("file")
    target_role = request.data.get("role", None)
    file_name = file.name if file else "unknown"

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        # Save file temporarily for Celery task
        tmp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        fs = FileSystemStorage(location=tmp_dir)
        filename = f"{uuid.uuid4()}_{file.name}"
        saved_filename = fs.save(filename, file)
        file_path = fs.path(saved_filename)

        user_id = request.user.id if request.user and request.user.is_authenticated else None

        # Dispatch Celery task
        task = analyze_resume_task.delay(file_path, target_role, file_name, user_id)

        return Response({
            "task_id": task.id,
            "status": "PENDING"
        })
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return Response({"error": f"Internal Server Error: {error_msg}"}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def check_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'SUCCESS':
        return Response({
            "status": task_result.state,
            "result": task_result.result
        })
    elif task_result.state == 'FAILURE':
        return Response({
            "status": task_result.state,
            "error": str(task_result.info)
        })
    else:
        return Response({
            "status": task_result.state
        })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analysis_history(request):
    analyses = ResumeAnalysis.objects.filter(user=request.user)
    serializer = ResumeAnalysisSerializer(analyses, many=True)
    return Response(serializer.data)
