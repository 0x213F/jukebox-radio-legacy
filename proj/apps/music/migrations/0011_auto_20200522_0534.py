# Generated by Django 3.0.3 on 2020-05-22 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_ticket_is_hidden_when_idle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='status',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('joined', 'Joined'), ('left', 'Left'), ('comment', 'Commented')], max_length=12),
        ),
    ]
