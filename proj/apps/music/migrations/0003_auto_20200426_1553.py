# Generated by Django 3.0.3 on 2020-04-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20200426_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='storage_img_high',
        ),
        migrations.AddField(
            model_name='record',
            name='storage_filename',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='storage_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
