# Generated by Django 2.2.6 on 2020-05-10 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elixr', '0002_auto_20200509_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedSuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('suit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elixr.Suit')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elixr.Ship')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('ord_ships', models.ManyToManyField(to='elixr.OrderedShip')),
                ('ord_suits', models.ManyToManyField(to='elixr.OrderedSuit')),
            ],
        ),
    ]
