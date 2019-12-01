
from datetime import datetime

from django import forms
from django.contrib import admin
from django.contrib import messages
from django import urls
from django.utils.html import format_html

from proj.apps.music.models import Record
from proj.apps.music.models import Showing

from proj.apps.music.admin.inline import RecordInline
from proj.apps.music.forms import ShowingForm


@admin.register(Showing)
class ShowingAdmin(admin.ModelAdmin):

    # - - - - -
    # display
    # - - - - -

    form = ShowingForm

    search_fields = (
        'id',
        'uuid',
        'title',
        'status__icontains',
    )

    list_display = (
        'title',
        'current_record',
        'time_left',
        'status',
        'uuid',
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.fields = (
                'title',
                'showtime_scheduled',
            )
            self.readonly_fields = ('',)
        elif obj.status == Showing.STATUS_IDLE:
            self.fields = (
                'title',
                'showtime_scheduled',
            )
            self.readonly_fields = ('title',)
        elif obj.status == Showing.STATUS_ACTIVATED:
            if obj.time_left_on_current_record:
                self.fields = (
                    'title',
                    'link_to_record',
                    'time_left',
                    'record_terminates_at',
                )
                self.readonly_fields = ('title', 'link_to_record', 'time_left', 'record_terminates_at',)
            else:
                self.fields = (
                    'title',
                    'current_record',
                    'time_left',
                    'record_terminates_at',
                )
                self.readonly_fields = ('title', 'link_to_record', 'time_left', 'record_terminates_at',)
        elif obj.status == Showing.STATUS_TERMINATED:
            fields = (
                'title',
                'showtime_scheduled',
                'current_record',
            )
            self.fields = fields
            self.readonly_fields = fields
        return super().get_form(request, obj, **kwargs)

    # inlines = [
    #     RecordInline,
    # ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('id')

    def link_to_record(self, showing):
        record = showing.current_record
        record_link = urls.reverse(
            'admin:music_record_change', args=[record.id]
        )
        return format_html(f'<button><a href="{record_link}">{record.name}</a></button>')

    def time_left(self, showing):
        return showing.time_left_on_current_record

    # - - - - -
    # actions
    # - - - - -

    actions = [
        'activate_selected_showing',
        'idle_selected_showing',
        'terminate_selected_showing',
    ]

    def activate_selected_showing(self, request, queryset):
        scheduled = (
            queryset
            .filter(
                status__in=(
                    Showing.STATUS_SCHEDULED,
                    Showing.STATUS_IDLE,
                )
            )
        )
        if queryset.count() != scheduled.count():
            self.message_user(
                request,
                'Make sure all showings are scheduled.',
                level=messages.ERROR,
            )
            return
        for showing in queryset:
            Showing.objects.change_status(showing, Showing.STATUS_ACTIVATED)
    activate_selected_showing.short_description = 'Activate selected showing'

    def idle_selected_showing(self, request, queryset):
        scheduled = (
            queryset
            .filter(status__in=(Showing.STATUS_ACTIVATED, Showing.STATUS_TERMINATED))
        )
        if queryset.count() != scheduled.count():
            self.message_user(
                request,
                'Make sure all showings are activated.',
                level=messages.ERROR,
            )
            return
        for showing in queryset:
            Showing.objects.change_status(showing, Showing.STATUS_IDLE)
    idle_selected_showing.short_description = 'Idle selected showing'

    def terminate_selected_showing(self, request, queryset):
        now = datetime.now()
        selection = (
            queryset.filter(
                status__in=(Showing.STATUS_ACTIVATED, Showing.STATUS_IDLE),
                record_terminates_at__lt=now,
            )
        )
        if queryset.count() != selection.count():
            self.message_user(
                request,
                'One or more of the selected showings are currently playing.',
                level=messages.ERROR,
            )
            return
        queryset.update(status=Showing.STATUS_TERMINATED)
    terminate_selected_showing.short_description = 'Terminate selected showing'

    # - - -
    # save
    # - - -

    def save_model(self, request, showing, form, change):
        '''
        Cache data from Spotify API.
        '''
        now = datetime.now()
        try:
            pre_save_showing = Showing.objects.get(id=showing.id)
            if pre_save_showing.current_record and pre_save_showing.record_terminates_at:
                if now < pre_save_showing.record_terminates_at.replace(tzinfo=None):
                    self.message_user(
                        request,
                        'The record cannot be changed since one is still playing.',
                        level=messages.ERROR,
                    )
                    return
        except Showing.DoesNotExist:
            pass

        current_record = form.cleaned_data['current_record']

        super().save_model(request, showing, form, change)

        if not current_record:
            return

        Showing.objects.spin(current_record, showing)
