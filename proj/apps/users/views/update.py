
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class UpdateView(BaseView):
    '''
    TODO docstring
    '''

    def post(self, request, **kwargs):
        '''
        TODO docstring
        '''
        display_name = request.POST.get('display_name', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)

        if display_name:
            request.user.profile.display_name = display_name
            request.user.profile.save()
        if first_name or last_name or email:
            if first_name:
                request.user.first_name = first_name
            if last_name:
                request.user.last_name = last_name
            if email:
                request.user.email = email
            request.user.save()
        return self.http_response({})
