# Generated by Django 5.1.1 on 2024-10-14 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0004_alter_character_prefered_partner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='character',
            old_name='prefered_partner',
            new_name='preferred_partner',
        ),
    ]