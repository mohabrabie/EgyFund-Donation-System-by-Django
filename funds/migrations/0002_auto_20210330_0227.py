# Generated by Django 3.1.7 on 2021-03-30 00:27

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='pictures',
        ),
        migrations.AddField(
            model_name='projectpicture',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.fields.NOT_PROVIDED, to='funds.project'),
            preserve_default=False,
        ),
    ]