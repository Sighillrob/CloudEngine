from push.push_service import DefaultNamespace
from socketio import socketio_manage
from django.http import HttpResponse





def socketio_view(request):
    socketio_manage(
        request.environ, {'/default': DefaultNamespace}, request=request)
    return HttpResponse()
