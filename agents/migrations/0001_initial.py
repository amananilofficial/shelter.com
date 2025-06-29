# Generated by Django 5.2.3 on 2025-06-20 18:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='agents/%Y/%m/%d')),
                ('title', models.CharField(default='Real Estate Agent', max_length=100)),
                ('description', models.TextField(blank=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('whatsapp', models.CharField(max_length=30)),
                ('instagram', models.CharField(max_length=100)),
                ('linkedin', models.CharField(max_length=100)),
                ('hire_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('work_experience', models.TextField(blank=True, help_text="Enter work experience points separated by the '|' character. Each point will be displayed as a separate bullet point on the frontend.")),
            ],
        ),
        migrations.CreateModel(
            name='AgentContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agentname', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_subject', models.TextField(max_length=200)),
                ('user_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgentPropertyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agentname', models.CharField(max_length=100)),
                ('property_title', models.CharField(max_length=200)),
                ('user_name', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_phone', models.CharField(max_length=20)),
                ('user_subject', models.TextField(max_length=200)),
                ('contact_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
