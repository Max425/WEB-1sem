# Generated by Django 4.1.7 on 2023-04-12 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='photo.png', upload_to='../static/css/img/'),
        ),
    ]
