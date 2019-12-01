
from datetime import datetime

from django import forms
from django.contrib import admin
from django.contrib import messages

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
            self.fields = (
                'title',
                'current_record',
                'time_left',
                'record_terminates_at',
            )
            self.readonly_fields = ('title', 'time_left', 'record_terminates_at',)
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

    def time_left(self, showing):
        now = datetime.now()
        dt = showing.record_terminates_at.replace(tzinfo=None)
        if not dt or now >= dt:
            return 'Not Playing'
        else:
            return dt - now

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
        already_terminated = (
            queryset.filter(
                status__in=(
                    Showing.STATUS_TERMINATED,
                )
            )
        )
        if already_terminated.exists():
            self.message_user(
                request,
                'Make sure all showings are not currently terminated.',
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

        print(showing.current_record)

        super().save_model(request, showing, form, change)

        if not current_record:
            return

        Showing.objects.spin(current_record, showing)
