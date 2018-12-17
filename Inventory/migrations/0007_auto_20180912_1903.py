# Generated by Django 2.0.5 on 2018-09-12 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0006_auto_20180911_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenotypeDownloads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='additions/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('download_pass', models.FileField(blank=True, upload_to='logs/')),
                ('download_fail', models.FileField(blank=True, upload_to='logs/')),
                ('issues', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='genotypes',
            name='comments',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='genotypeuploads',
            name='issues',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
