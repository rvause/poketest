# Generated by Django 3.0.2 on 2020-01-28 13:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('types', models.CharField(max_length=255)),
                ('image_url', models.URLField(max_length=255)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
