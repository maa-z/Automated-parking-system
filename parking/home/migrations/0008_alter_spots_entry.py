# Generated by Django 5.0.2 on 2024-05-27 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_spots_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spots',
            name='entry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
