from django.contrib import admin

from proj.apps.music.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    # - - - - -
    # display
    # - - - - -

    search_fields = ('text',)

    list_display = (
        'commenter',
        'status',
        'text',
        'track',
        'track_timestamp',
        'stream',
        'created_at',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('id')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
