# Generated by Django 5.2.3 on 2025-06-21 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_worknote'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='is_mvp',
            field=models.BooleanField(default=False, help_text='Whether this agent is an MVP (Most Valuable Player)'),
        ),
    ]
