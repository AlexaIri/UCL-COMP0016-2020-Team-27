# Generated by Django 3.1.5 on 2021-03-13 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CFP_Portal', '0028_person_evidence'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='github',
            field=models.URLField(blank=True, verbose_name='github link'),
        ),
    ]
