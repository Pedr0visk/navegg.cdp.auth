# Generated by Django 3.2.7 on 2021-11-01 13:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_accounts_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='accounts_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]
