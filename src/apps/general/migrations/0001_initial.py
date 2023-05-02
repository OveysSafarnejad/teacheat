# Generated by Django 4.2 on 2023-05-02 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='Modify time')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
    ]