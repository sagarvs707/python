# Generated by Django 2.1.7 on 2019-04-11 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viyaan_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signup',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='address',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='last_name',
        ),
    ]