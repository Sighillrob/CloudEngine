# Create your views here.

import logging
import json
<<<<<<< HEAD
from pymongo import MongoClient
from bson.objectid import ObjectId
from rest_framework.response import Response
from rest_framework import status
from core.cloudapi_view import CloudAPIView
=======
import csv
import cStringIO as StringIO
#from rest_framework.views import APIView
from core.cloudapi_view import CloudAPIView
from core.models import CloudApp
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView, View
from django.shortcuts import  redirect
from django.http import HttpResponse
from classes.forms import FileUploadForm
from manager import ClassesManager
from classes.utils import validate_db_name
from classes.csv_unicode import DictWriter
>>>>>>> 14181f4... order query results in ascending/descending manner

logger = logging.getLogger("cloudengine")


class AppClassesView(CloudAPIView):

    def get(self, request):
        app = request.META['app']
        db_name = app.name
        client = MongoClient()
        db = client[db_name]
        app_classes = db.collection_names(include_system_collections=False)
        return Response({"result": app_classes})


class ClassView(CloudAPIView):

<<<<<<< HEAD
=======
    DEFAULT_QUERY = '{}'

>>>>>>> 14181f4... order query results in ascending/descending manner
    def get(self, request, cls):
        app = request.META['app']
        db_name = app.name
        client = MongoClient()
        db = client[db_name]
        collection = db[cls]
        # Django automatically urldecodes query string
        query_str = request.GET.get('query', '{}')
        logger.info("query string received: %s" % query_str)
        try:
            # urlparse the query
            query = json.loads(query_str)
        except Exception:
            return Response({"detail": "Invalid query"},
                            status=status.HTTP_400_BAD_REQUEST,
                            exception=True)
<<<<<<< HEAD
=======
        
        
        try:
            # urlparse the query
            order_str = request.GET['orderby']
            order_obj = json.loads(order_str)
            assert(len(order_obj) == 1)      # sorting possible only on one key
            order_by = order_obj.keys()[0]
            order = order_obj.values()[0]
        except AssertionError:
            return Response({'detail': 'orderby option takes only one property value'},
                            status=status.HTTP_400_BAD_REQUEST,
                            exception=True)
        except Exception, e:
            order_by = order = None
        try:
            res = manager.get_class(db_name, app, cls, query, order_by, order)
        except Exception, e:
            return Response({'detail': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            exception=True)
        return Response({"result": res})
>>>>>>> 14181f4... order query results in ascending/descending manner

        cursor = collection.find(query)      # app_id is used only by server
        res = [doc for doc in cursor]

        for doc in res:
            objid = doc["_id"]
            doc["_id"] = str(objid)

        return Response({"result": res})

    def delete(self, request, cls):
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'detail': 'App id not provided'}, status=401)

        client = MongoClient()

        db_name = app.name
        db = client[db_name]
        if cls in db.collection_names():
            collection = db[cls]
            collection.remove()

        return Response()

    def post(self, request, cls):
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'detail': 'App id not provided'}, status=401)
        client = MongoClient()
        db_name = app.name
        db = client[db_name]
        collection = db[cls]
        try:
            logger.debug("request body recieved: %s" % request.body)
            new_obj = json.loads(request.body)

        except Exception, e:
            logger.error("Unable to decode object. Error: %s" % str(e))
            return Response({"detail": "Invalid object."},
                            status=status.HTTP_400_BAD_REQUEST,
                            exception=True)
        if "_id" in new_obj.keys():
            return Response({
                    "detail": "Invalid object. _id is a reserved field"},
                    status=status.HTTP_400_BAD_REQUEST
                                )
            
        objid = collection.insert(new_obj)
        return Response({"_id": str(objid)}, status=201)


class ObjectView(CloudAPIView):

    def get(self, request, cls, objid):
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'detail': 'App id not provided'}, status=401)

        client = MongoClient()
        db_name = app.name
        db = client[db_name]
        collection = db[cls]
        obj = collection.find_one({"_id": ObjectId(objid)})
        if obj:
            objid = obj["_id"]
            obj["_id"] = str(objid)
            return Response({"result": obj})
        else:
            return Response({"detail": "Invalid object id"},
                            status=status.HTTP_400_BAD_REQUEST,
                            exception=True)

    # todo: put should actually replace the existing objects
    # since updating only a few fields does not affect the existing fields, in
    # case the user wanted to delete a few fields. Android: Object.remove()
    def put(self, request, cls, objid):
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'detail': 'App id not provided'}, status=401)

        client = MongoClient()
        db_name = app.name
        db = client[db_name]
        collection = db[cls]
        try:
            obj = json.loads(request.body)
        except Exception:
            return Response({"detail": "Invalid object id"},
                            status=status.HTTP_400_BAD_REQUEST,
                            exception=True)
        if "_id" in obj.keys():
            return Response({
                    "detail": "Invalid object. _id is a reserved field"},
                    status=status.HTTP_400_BAD_REQUEST
                                )
            
        collection.update({"_id": ObjectId(objid)},
                          {"$set": obj})               
        return Response()

    def delete(self, request, cls, objid):
        app = request.META.get('app', None)
        if not app:
            # We should not have reached here anyway
            return Response({'detail': 'App id not provided'}, status=401)

        client = MongoClient()
        db_name = app.name
        db = client[db_name]
        collection = db[cls]
        collection.remove(ObjectId(objid))
        return Response()
