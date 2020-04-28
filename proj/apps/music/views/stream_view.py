from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from io import BytesIO
from django.http import FileResponse
from boto3 import session

from django.conf import settings

from proj.core.views import BaseView
from proj.core.resources import Spotify
from proj.core.resources import YouTube


@method_decorator(login_required, name='dispatch')
class StreamView(BaseView):
    def get(self, request, **kwargs):
        '''
        Search a user's library
        '''
        Record = apps.get_model('music', 'Record')

        storage_id = request.GET.get('storage_id', None)

        record = Record.objects.get(storage_id=storage_id)

        session2 = session.Session()
        client = session2.client('s3',
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=f'https://{settings.AWS_S3_REGION_NAME}.digitaloceanspaces.com',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        obj = client.get_object(
            Bucket='jukebox-radio-space', Key=record.storage_filename
        )

        return FileResponse(BytesIO(obj['Body'].read()))
