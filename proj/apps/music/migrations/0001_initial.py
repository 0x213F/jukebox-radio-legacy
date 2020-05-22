# Generated by Django 3.0.3 on 2020-03-28 21:03

import datetime
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=128)),
                ("spotify_uri", models.CharField(max_length=128)),
                ("spotify_img", models.CharField(max_length=256)),
                ("is_playing", models.BooleanField(default=False)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Stream",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("title", models.CharField(max_length=128)),
                (
                    "unique_custom_id",
                    models.CharField(blank=True, max_length=64, null=True, unique=True),
                ),
                ("owner_name", models.CharField(max_length=128)),
                ("tags", models.CharField(max_length=128)),
                ("is_private", models.BooleanField(default=False)),
                ("showtime_actual", models.DateTimeField(null=True)),
                ("last_status_change_at", models.DateTimeField(blank=True, null=True)),
                ("record_terminates_at", models.DateTimeField(null=True)),
                ("status", models.CharField(default="idle", max_length=128)),
                (
                    "current_record",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="now_playing_at_streams",
                        to="music.Record",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="owned_streams",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("spotify_uri", models.CharField(max_length=64)),
                ("spotify_name", models.CharField(max_length=256)),
                ("spotify_duration_ms", models.PositiveIntegerField()),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="TrackListing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("number", models.PositiveIntegerField()),
                (
                    "record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracks_through",
                        to="music.Record",
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="records_through",
                        to="music.Track",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("track", "record", "number")},
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("email", models.CharField(editable=False, max_length=64)),
                ("name", models.CharField(editable=False, max_length=32)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("is_administrator", models.BooleanField(default=False)),
                ("is_subscribed", models.BooleanField(default=False)),
                ("is_listed", models.BooleanField(default=False)),
                ("status", models.CharField(editable=False, max_length=32)),
                ("updated_at", models.DateTimeField(null=True)),
                ("holder_uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "holder",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="tickets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "stream",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="tickets",
                        to="music.Stream",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.AddField(
            model_name="record",
            name="tracks",
            field=models.ManyToManyField(
                through="music.TrackListing", to="music.Track"
            ),
        ),
        migrations.AddField(
            model_name="record",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="records",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Queue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                ("played_at", models.DateTimeField(blank=True, null=True)),
                (
                    "record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="queued",
                        to="music.Record",
                    ),
                ),
                (
                    "stream",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="queued",
                        to="music.Stream",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="queued",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("joined", "Joined"),
                            ("waited", "Waited"),
                            ("left", "Left"),
                            ("activated", "Activated"),
                            ("idle", "Idle"),
                            ("low", ":("),
                            ("mid_low", ":/"),
                            ("neutral", ":|"),
                            ("mid_high", ":)"),
                            ("high", ":D"),
                            ("spin", "Spinning"),
                            ("stop", "Stopped"),
                            ("start", "Started"),
                            ("play", "Played"),
                            ("pause", "Paused"),
                            ("neutral", "Neutral"),
                            ("next", "Skipped"),
                            ("prev", "Backtracked"),
                            ("queue", "Queued"),
                        ],
                        max_length=12,
                    ),
                ),
                ("text", models.TextField(blank=True, null=True)),
                ("track_timestamp", models.DurationField(blank=True, null=True)),
                (
                    "commenter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "commenter_ticket",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="commenter_tickets",
                        to="music.Ticket",
                    ),
                ),
                (
                    "record",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="spins",
                        to="music.Record",
                    ),
                ),
                (
                    "stream",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="comments",
                        to="music.Stream",
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="comments",
                        to="music.Track",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
