# Generated by Django 2.0.5 on 2018-08-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0003_auto_20180807_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genotypes',
            name='actual_count',
            field=models.BooleanField(default=False),
        ),
    ]