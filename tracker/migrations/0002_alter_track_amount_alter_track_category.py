# Generated by Django 4.1.6 on 2023-04-10 13:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(-100000000), django.core.validators.MaxValueValidator(100000000)]),
        ),
        migrations.AlterField(
            model_name='track',
            name='category',
            field=models.CharField(choices=[('unsorted', 'Unsorted'), ('education', 'Education'), ('food', 'Food'), ('wallet', 'Wallet')], default='unsorted', max_length=10),
        ),
    ]