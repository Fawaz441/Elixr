# Generated by Django 2.2.6 on 2020-05-10 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elixr', '0003_order_orderedship_orderedsuit'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elixr.Buyer'),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
    ]