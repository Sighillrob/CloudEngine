from rest_framework import serializers
from models import CloudApp

class CloudAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudApp
        read_only_fields = ('key',)
    
    
        