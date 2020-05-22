from django.contrib import admin

from proj.apps.music.models import Stream


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):

    # - - - - -
    # display  |
    # - - - - -

    search_fields = (
        "id",
        "uuid",
        "title",
        "status__icontains",
    )

    list_display = (
        "title",
        "status",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")
