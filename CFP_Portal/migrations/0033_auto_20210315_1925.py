# Generated by Django 3.1.5 on 2021-03-15 19:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CFP_Portal', '0032_auto_20210314_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='reviewers',
            field=models.ManyToManyField(blank=True, related_name='reviewers', to=settings.AUTH_USER_MODEL),
        ),
    ]
