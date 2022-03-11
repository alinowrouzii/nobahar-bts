# Generated by Django 3.2 on 2022-03-11 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_group_groupconnectionrecord_message_userjoinrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userjoinrecord',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_records', to='app1.group'),
        ),
        migrations.AlterField(
            model_name='userjoinrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_records', to=settings.AUTH_USER_MODEL),
        ),
    ]