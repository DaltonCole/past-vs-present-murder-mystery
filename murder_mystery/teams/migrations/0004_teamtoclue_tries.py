# Generated by Django 5.1.1 on 2024-10-16 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_teamtoclue'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamtoclue',
            name='tries',
            field=models.SmallIntegerField(default=0),
        ),
    ]