# Generated by Django 2.1.15 on 2020-12-07 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Menu_Dien_Tu_App', '0007_table_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='user',
        ),
    ]
