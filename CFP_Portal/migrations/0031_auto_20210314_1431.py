# Generated by Django 3.1.5 on 2021-03-14 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CFP_Portal', '0030_merge_20210313_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='git',
        ),
        migrations.AddField(
            model_name='person',
            name='reviewers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to=settings.AUTH_USER_MODEL),
        ),
    ]