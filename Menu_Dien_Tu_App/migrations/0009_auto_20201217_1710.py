# Generated by Django 2.1.15 on 2020-12-17 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Menu_Dien_Tu_App', '0008_remove_table_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='describeitem',
            name='menuItem',
        ),
        migrations.DeleteModel(
            name='DescribeItem',
        ),
    ]
