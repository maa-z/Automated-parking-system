# Generated by Django 5.0.2 on 2024-02-27 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_slots'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='cost',
            field=models.IntegerField(null=True),
        ),
    ]
