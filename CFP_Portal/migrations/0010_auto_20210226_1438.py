# Generated by Django 3.1.5 on 2021-02-26 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CFP_Portal', '0009_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='feedback',
        ),
    ]
