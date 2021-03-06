# Generated by Django 2.0.5 on 2018-09-10 18:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('filepath', models.FileField(null=True, upload_to='files/', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Genotypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_f_row', models.CharField(max_length=200)),
                ('parent_m_row', models.CharField(max_length=200)),
                ('parent_f_geno', models.CharField(max_length=200)),
                ('parent_m_geno', models.CharField(max_length=200)),
                ('genotype', models.CharField(max_length=200)),
                ('seed_count', models.IntegerField(default=0)),
                ('actual_count', models.BooleanField(default=False)),
                ('experiment', models.CharField(blank=True, max_length=200)),
                ('comments', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Genotypes',
            },
        ),
        migrations.CreateModel(
            name='GenotypeUploads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='additions/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(code='invalid', message='Needs to start with WOW', regex='^WOW')])),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
