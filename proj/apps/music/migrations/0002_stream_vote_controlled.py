# Generated by Django 3.0 on 2020-01-20 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='vote_controlled',
            field=models.BooleanField(default=False),
        ),
    ]
