# Generated by Django 3.0.8 on 2020-09-06 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='date_ordered',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_ordered',
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]