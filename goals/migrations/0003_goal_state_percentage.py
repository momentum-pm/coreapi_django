# Generated by Django 4.2.7 on 2023-12-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_delete_responsibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='state_percentage',
            field=models.FloatField(default=0),
        ),
    ]