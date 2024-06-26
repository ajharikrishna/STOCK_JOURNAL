# Generated by Django 3.0 on 2024-06-03 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('stock_symbol', models.CharField(max_length=10)),
                ('trade_type', models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')], max_length=4)),
                ('entry_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('exit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('position_size', models.IntegerField()),
                ('trade_rationale', models.TextField()),
                ('trade_outcome', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
    ]
