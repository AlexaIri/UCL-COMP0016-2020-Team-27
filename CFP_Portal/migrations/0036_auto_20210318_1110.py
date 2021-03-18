# Generated by Django 2.2 on 2021-03-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CFP_Portal', '0035_underreviewprojects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Under Review', 'Under Review'), ('Submitted', 'Submitted'), ('Resubmit', 'Resubmit')], default='', max_length=20, verbose_name='What is the current status of the project?'),
        ),
    ]
