# Generated by Django 3.1.5 on 2021-03-10 14:48

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('CFP_Portal', '0020_auto_20210310_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rejectedprojects',
            old_name='date_rejected',
            new_name='date_accepted',
        ),
        migrations.RemoveField(
            model_name='acceptedprojects',
            name='id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='hashtags',
        ),
        migrations.RemoveField(
            model_name='rejectedprojects',
            name='id',
        ),
        migrations.AddField(
            model_name='person',
            name='NICEtier',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default='', max_length=20, verbose_name='What is the NICE tier of the project?'),
        ),
        migrations.AddField(
            model_name='person',
            name='challenge',
            field=models.TextField(blank=True, default='', verbose_name='Is this project from a challenge?'),
        ),
        migrations.AddField(
            model_name='person',
            name='department',
            field=models.CharField(blank=True, default='', max_length=2000, verbose_name='department'),
        ),
        migrations.AddField(
            model_name='person',
            name='organisation',
            field=models.CharField(blank=True, default='', max_length=2000, verbose_name='organisation'),
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='person',
            name='title',
            field=models.CharField(default='', max_length=130, verbose_name='job title'),
        ),
        migrations.AlterField(
            model_name='acceptedprojects',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='project', serialize=False, to='CFP_Portal.person'),
        ),
        migrations.AlterField(
            model_name='rejectedprojects',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='CFP_Portal.person'),
        ),
    ]
