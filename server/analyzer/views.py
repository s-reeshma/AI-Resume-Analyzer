import os
import uuid
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from celery.result import AsyncResult
from .tasks import analyze_resume_task

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_resume(request):
    file = request.FILES.get("file")
    target_role = request.data.get("role", None)

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        # Save file temporarily for Celery task
        from django.conf import settings
        tmp_dir = os.path.join(settings.BASE_DIR, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        fs = FileSystemStorage(location=tmp_dir)
        filename = f"{uuid.uuid4()}_{file.name}"
        saved_filename = fs.save(filename, file)
        file_path = fs.path(saved_filename)

        # Dispatch Celery task
        task = analyze_resume_task.delay(file_path, target_role)

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