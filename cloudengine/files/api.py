import logging
from models import CloudFile
from manager import FilesManager
from exceptions import FileTooLarge, FileNotFound
from cloudengine.core.models import CloudApp
from cloudengine.core.cloudapi_view import CloudAPIView
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import generics
from serializers import CloudFileSerializer

logger = logging.getLogger("cloudengine")

AWS_URL_EXPIRY = 3600 * 24 * 265 * \
    20         # won't expire for a very long time

#todo: test that cloudapi is compatible with generic
class FileListView(CloudAPIView, generics.ListCreateAPIView):
    serializer_class = CloudFileSerializer

    def get(self, request, *args, **kwargs):
        app = request.META.get('app', None)             #todo: handle checking of appid present in a middleware
        if not app:
            return Response({"error": "Invalid app id provided"},
                            status=400)
        cloudapp = CloudApp.objects.get(name=app.name)
        self.queryset = CloudFile.objects.filter(app=cloudapp)
        return super(FileListView, self).get(request, *args, **kwargs)


# make sure filename in the newly generated url (before query string) does
# end with trailing slash
# S3 is hard coded now. Allow other storages to be plugged in
class FileView(CloudAPIView):

    manager = FilesManager()
    
    def get(self, request, filename):
        usr = request.user.username
        logger.info("file get received from user %s for file %s" %(usr, filename))
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'error': 'App id not provided'}, status=401)
        try:
            cloudfile = CloudFile.objects.get(name=filename, app=app)
        except CloudFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)
        return Response({"url": cloudfile.url})
    
    
    def post(self, request, filename):
        content_length = request.META.get("CONTENT_LENGTH", 0)
        content_length = int(content_length)
        body = request.body
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'error': 'App id not provided'}, status=401)
        cont_file = ContentFile(body)
        try:
            url = self.manager.upload(filename, cont_file, app)
        except FileTooLarge as e:
            return Response({'error': str(e)}, 
                            status=401)
        except Exception:
            return Response({'error': 'Error uploading file'}, status=500)

        return Response({"url": url}, status=201)
    
    def delete(self, request, filename):
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'error': 'App id not provided'}, status=401)
        try:
            self.manager.delete(filename, app)
        except FileNotFound as e:
            return Response({'error': str(e)}, status=404)
        except Exception:
            return Response({'error': 'Error deleting file'}, status=500)
        return Response({"result": "File deleted successfully"})


