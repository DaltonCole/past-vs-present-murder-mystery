# Generated by Django 5.1.1 on 2024-10-09 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='password',
        ),
    ]
