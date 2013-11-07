import logging
from django.http import HttpRequest
from rest_framework.views import APIView
from socketio.namespace import BaseNamespace


# This mixin creates a separate channel for each user/app
class UserChannelMixin(object):

    def __init__(self, *args, **kwargs):
        super(UserChannelMixin, self).__init__(*args, **kwargs)
        if 'channels' not in self.session:
            self.session['channels'] = set()  # a set of simple strings

    def subscribe(self, channel):
        """Lets a user subscribe to a channel on a specific Namespace."""
        self.session['channels'].add(self._get_channel_name(channel))

    def unsubscribe(self, channel):
        """Lets a user unsubscribe from a channel on a specific Namespace."""
        self.session['channels'].remove(self._get_channel_name(channel))

    def _get_channel_name(self, channel):
        return self.ns_name + '_' + channel

    def emit_to_channel(self, channel, event, *args):
        """This is sent to all subscribers of the channel (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        channel_name = self._get_channel_name(channel)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'channels' not in socket.session:
                continue
            if channel_name in socket.session['channels'] and self.socket != socket:
                socket.send_packet(pkt)


class DefaultNamespace(BaseNamespace, UserChannelMixin):

    def initialize(self):
        self.logger = logging.getLogger("cloudengine")
        auth_id = self.authenticate_request()
        if auth_id:
            self.logger.info("initializing socketio for user %s" % auth_id)
            self.lift_acl_restrictions()
            self.channel = auth_id
            #self._objects[id(self)] = self
            # currently every user is automatically subscribed to the default
            # channel
            self.subscribe(self.channel)
            self.emit('connect')
        else:
            self.logger.info("user not authenticated in socketio:initlaize")
            return

    def on_subscribe(self):
        self.logger.info("subscibing on channel %s" % self.channel)
        self.subscribe(self.channel)

    def on_unsubscribe(self):
        self.logger.info("unsubscibing on channel %s" % self.channel)
        self.unsubscribe(self.channel)

    # request = saved request from previous call for session authentication
    def authenticate_request(self):
        auth_id = self.perform_authentication(self.request)
        if auth_id:
            return auth_id
        # try token authentication
        req = HttpRequest()
        req.META = self.socket.handshake_environ
        return self.perform_authentication(req)

    # django-rest-framework doesn't have a explicit API for authentication
    # besides API views. Simulate that.
    def perform_authentication(self, request):
        myview = APIView()
        init_request = myview.initialize_request(request)
        myview.perform_authentication(init_request)
        return init_request.user.username

    def get_initial_acl(self):
        return []

    # def disconnect(self, *args, **kwargs):
    #    try:
    #        del self._objects[id(self)]
    #    except KeyError:
    #        pass
    #   super(PushNamespace, self).disconnect(*args, **kwargs)

    def on_send(self, message):
        # for s in self._objects.values():
        self.logger.info("sending push msg %s to channel %s" %
                         (message, self.channel))
        self.emit_to_channel(self.channel, "push", message)
        #self.emit( 'push', message)
        return True
