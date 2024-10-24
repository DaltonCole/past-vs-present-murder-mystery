# Generated by Django 5.1.1 on 2024-10-24 00:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('story_clues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=32)),
                ('location_hint1', models.TextField()),
                ('location_hint2', models.TextField()),
                ('location_hint3', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LocationClue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location_clues.location')),
                ('story_clue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story_clues.storyclue')),
            ],
        ),
    ]