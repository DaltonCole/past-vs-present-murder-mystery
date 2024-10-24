# Generated by Django 5.1.1 on 2024-10-24 00:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('characters', '0001_initial'),
        ('story_clues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptorFlavorText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OccupationFlavorText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CharacterClue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.character')),
                ('story_clue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story_clues.storyclue')),
                ('descriptor1_flavor_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descriptor1', to='character_clues.descriptorflavortext')),
                ('descriptor2_flavor_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descriptor2', to='character_clues.descriptorflavortext')),
                ('descriptor3_flavor_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descriptor3', to='character_clues.descriptorflavortext')),
                ('occupation_flavor_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='occupation', to='character_clues.occupationflavortext')),
            ],
        ),
    ]