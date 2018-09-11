# Generated by Django 2.0.5 on 2018-09-11 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genotypeuploads',
            name='issues',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='genotypeuploads',
            name='upload_fail',
            field=models.FileField(blank=True, upload_to='additions/'),
        ),
        migrations.AddField(
            model_name='genotypeuploads',
            name='upload_pass',
            field=models.FileField(blank=True, upload_to='additions/'),
        ),
    ]
