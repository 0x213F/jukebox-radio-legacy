
import json

from django.core.serializers import serialize

from django.db import models


class BaseManager(models.Manager):
    '''
    Inherits from Django Manager.
    '''

    def do(self, action, request):
        '''
        Used to wire up the generic POST endpoint (see below) to its manager
        method. The `user` argument is authenticated through the request.

        /do?thing=baz&with_action={'foo':'bar'}

        - thing:        the manager method to be called
        - with_action:  **kwargs passed to the manager method
        '''

        if not request.user:
            raise Exception('User must be authenticated.')

        do_thing = getattr(self, action.replace('-', '_'))
        kwargs = json.loads(request.POST.get('with_args', '{}'))
        kwargs['user'] = request.user

        return do_thing(**kwargs)

    def response(self, result):
        '''
        Subclass this method to transform a response object into a JSON object.
        '''
        return json.dumps(serialize('json', [result]))
