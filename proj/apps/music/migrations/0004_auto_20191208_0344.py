# Generated by Django 3.0 on 2019-12-08 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20191208_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spins', to='music.Record'),
        ),
    ]
