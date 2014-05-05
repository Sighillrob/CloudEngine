from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from cloudengine.core.models import CloudApp
from cloudengine.classes.manager import ClassesManager
from cloudengine.files.utils import delete_app_files


# View for creating new apps
class AppView(APIView):

    def post(self, request, name):
        app = CloudApp(name=name)
        app.save()
        return Response({"id": app.key})
    

    def delete(self, request, name):
        try:
            # ensure that an app with this name doesn't already exist
            app = CloudApp.objects.get(user = request.user, name= name)
        except CloudApp.DoesNotExist:
            return Response({"error": "App does not exist"},
                            status=status.HTTP_401_UNAUTHORIZED
                            )
        # delete all app data
        manager = ClassesManager()
        db = request.user.username
        manager.delete_app_data(db, app)
        # delete files
        delete_app_files(app)
        #delete app object
        app.delete()
        return Response({"result": "App deleted successfully"})


class AppListView(APIView):

    def get(self, request):
        app_props = ['name', 'key']
        app_list = []
        apps = CloudApp.objects.all()
        for app in apps:
            new_app = {}
            for prop in app_props:
                new_app[prop] = getattr(app, prop)
            app_list.append(new_app)
        return Response({'result': app_list})
