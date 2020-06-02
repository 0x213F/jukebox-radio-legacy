# Generated by Django 3.0.3 on 2020-05-29 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0014_auto_20200526_1934"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="soundcloud_duration_ms",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="record",
            name="soundcloud_id",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="record",
            name="soundcloud_img",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="record",
            name="soundcloud_name",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
