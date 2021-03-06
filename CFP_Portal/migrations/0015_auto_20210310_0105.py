# Generated by Django 2.2 on 2021-03-10 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CFP_Portal', '0014_auto_20210309_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.CharField(choices=[('Accepeted', 'Accepted'), ('Rejected', 'Rejected'), ('Under Review', 'Under Review'), ('Submitted', 'Submitted'), ('Paused', 'Paused'), ('Reviewed', 'Reviewed')], default='', max_length=20, verbose_name='What is the current status of the project?'),
        ),
    ]
