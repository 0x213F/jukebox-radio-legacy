from django.contrib import admin

from proj.apps.music.models import TrackListing


@admin.register(TrackListing)
class TrackListingAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("record_id", "number")
