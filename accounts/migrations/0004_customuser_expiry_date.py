# Generated by Django 5.0.2 on 2024-02-25 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_payment_date_customuser_payment_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]