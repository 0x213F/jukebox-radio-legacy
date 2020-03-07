from cryptography.fernet import Fernet
from datetime import datetime
import requests
import uuid
from urllib.parse import urlparse

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime
from random_username.generate import generate_username


from proj.core.views import BaseView
from proj.core.resources import Spotify


@method_decorator(login_required, name="dispatch")
class SearchLibraryView(BaseView):

    def get(self, request, **kwargs):
        """
        Search the user's library.
        """
        query = request.GET.get("query", None)
        type = request.GET.get("type", None)

        spotify = Spotify(request.user)
        search_results = spotify.search_library(query, type)

        return self.http_response({
            'search_results': search_results,
            'type': type,
        })
