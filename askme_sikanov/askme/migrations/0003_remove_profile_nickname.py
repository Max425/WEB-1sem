# Generated by Django 4.1.7 on 2023-04-12 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0002_remove_profile_avatar_url_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nickname',
        ),
    ]