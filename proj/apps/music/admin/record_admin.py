from django.contrib import admin

from proj.apps.music.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

    # - - - - -
    # display  |
    # - - - - -

    search_fields = (
        'id',
        'name__icontains',
    )

    list_display = (
        'spotify_name',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('id')
