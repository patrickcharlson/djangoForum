# Generated by Django 4.0.3 on 2022-04-09 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_alter_profile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]