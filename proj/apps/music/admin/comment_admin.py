from django import forms
from django.contrib import admin
from django.contrib import messages

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    ChoiceDropdownFilter,
    RelatedDropdownFilter,
)

from proj.apps.music.models import Comment

from proj.apps.music.forms import CommentForm


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    # - - - - -
    # display
    # - - - - -

    form = CommentForm

    search_fields = ("text",)

    list_display = (
        "commenter",
        "status",
        "text",
        "track",
        "track_timestamp",
        "stream",
        "created_at",
    )

    list_filter = (
        # for related fields
        ("commenter", RelatedDropdownFilter),
        ("stream", RelatedDropdownFilter),
        ("track", RelatedDropdownFilter),
        ("status", DropdownFilter),
    )

    def get_list_display_links(self, request, list_display):
        """
        Makes the admin readonly with no link to change view.
        """
        return (None,)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
