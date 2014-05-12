from rest_framework import generics
from cloudengine.core.models import CloudApp
from django.conf import settings
from serializers import CloudAppSerializer


class AppListView(generics.ListCreateAPIView):
    queryset = CloudApp.objects.all()
    paginate_by = settings.PAGINATE_BY
    serializer_class = CloudAppSerializer
