# Generated by Django 3.0.3 on 2020-05-02 04:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20200430_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]