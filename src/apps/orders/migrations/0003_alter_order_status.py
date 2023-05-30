# Generated by Django 4.2 on 2023-05-30 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Registered'), (1, 'Rejected'), (2, 'Canceled'), (3, 'Accepted'), (4, 'Not Accepted')], default=0),
        ),
    ]