# Generated by Django 3.0 on 2020-03-19 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_ticket_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='unique_custom_id',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]
