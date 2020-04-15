from django.contrib import admin

from proj.apps.music.models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):

    # - - - - -
    # display  |
    # - - - - -

    search_fields = (
        "spotify_uri__exact",
        "spotify_name__icontains",
        "record__name__icontains",
    )

    list_display = (
        "name",
        "spotify_uri",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")

    def has_delete_permission(self, request, obj=None):
        return False

    def name(self, track):
        return track.spotify_name
