from django.db import models
from core.models import  CloudApp
from cloudengine.settings import REMOTE_FILES_DIR


class CloudFile(models.Model):
    name = models.CharField(max_length=200)
    content = models.FileField(upload_to=REMOTE_FILES_DIR)
    url = models.CharField(max_length=2000)
    size = models.BigIntegerField()
    app = models.ForeignKey(CloudApp)
