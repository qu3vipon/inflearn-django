# Generated by Django 5.1.3 on 2024-11-25 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_orm', '0009_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='preferences',
            field=models.JSONField(default=dict),
        ),
    ]
