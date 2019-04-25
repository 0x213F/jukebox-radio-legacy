
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

        # TODO: this is poor design. create a view that does authentication.
        #       once the request has been authenticated, then call the manager
        #       method. if there are similar authentication patterns, those
        #       could be pulled out into methods at the developer's discretion
        if not request.user:
            raise Exception('User must be authenticated.')

        do_thing = getattr(self, action.replace('-', '_'))
        kwargs = json.loads(request.POST.get('with_args', '{}'))
        kwargs['user'] = request.user

        return do_thing(**kwargs)

    def response(self, results):
        '''
        Subclass this method to transform a response object into a JSON object.
        '''
        results = json.loads(serialize('json', results))
        return results[0] if len(results) == 1 else results
