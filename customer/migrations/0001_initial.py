# Generated by Django 3.2.1 on 2021-05-06 09:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
            ],
            options={
                'db_tablespace': 'customer_company',
            },
        ),
        migrations.CreateModel(
            name='Evalution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30)),
                ('evalution_time', models.DateTimeField()),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.company')),
            ],
            options={
                'db_tablespace': 'customer_evalution',
            },
        ),
    ]