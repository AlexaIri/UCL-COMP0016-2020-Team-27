# Generated by Django 2.2 on 2021-03-17 01:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CFP_Portal', '0034_auto_20210315_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnderReviewProjects',
            fields=[
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='CFP_Portal.Person')),
                ('date_under_review', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]