# Generated by Django 5.0.2 on 2024-12-15 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_profile_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment_post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
    ]