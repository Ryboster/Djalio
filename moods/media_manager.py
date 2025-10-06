from django.views.decorators.csrf import csrf_exempt
import uuid
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

IMAGES_DIR = "images"
VIDEOS_DIR = "videos"
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
ALLOWED_VIDEO_EXTENSIONS = ['webm', 'mp4', 'ogg', 'avi', 'mov']
UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, IMAGES_DIR), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, VIDEOS_DIR), exist_ok=True)


def GetFileExtension(upload):
        filename = upload.name.lower()
        ext = filename.split('.')[-1] if '.' in filename else ''
        return ext

@csrf_exempt
def UploadMedia(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        
        uploadedFile = request.FILES['upload']
        extension = GetFileExtension(uploadedFile)
        
        # Check if extension is allowed
        if not (extension in ALLOWED_VIDEO_EXTENSIONS 
           or extension in ALLOWED_IMAGE_EXTENSIONS):
            return JsonResponse({
                'uploaded': False,
                'error': f'File extension not allowed: .{extension}. Supported: {", ".join(ALLOWED_VIDEO_EXTENSIONS + ALLOWED_IMAGE_EXTENSIONS)}'
            }, status=400)
            
        file_path = ""
        unique_filename = f"{uuid.uuid4()}.{extension}"
            
        if extension in ALLOWED_IMAGE_EXTENSIONS:
            file_path = os.path.join("uploads", IMAGES_DIR, unique_filename)
        elif extension in ALLOWED_VIDEO_EXTENSIONS:
            file_path = os.path.join("uploads", VIDEOS_DIR, unique_filename)
        
        try:
            path = default_storage.save(file_path, ContentFile(uploadedFile.read()))
            url = request.build_absolute_uri(settings.MEDIA_URL + path)
            return JsonResponse({
                'uploaded': True,
                'url': url,
                'filename': unique_filename,
                'is_video': extension in ALLOWED_VIDEO_EXTENSIONS
            })
        except Exception as e:
            return JsonResponse({
                'uploaded': False,
                'error': f'Upload failed: {str(e)}'
            }, status=500)
    return JsonResponse({
        'uploaded': False,
        'error': 'Invalid request - no file uploaded'
    }, status=400)
    