# Generated by Django 2.1.5 on 2020-01-26 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='vat_rate',
        ),
    ]
