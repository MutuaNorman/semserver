# Generated by Django 5.0.2 on 2024-02-24 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
    ]