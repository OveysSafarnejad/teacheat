# Generated by Django 4.2 on 2023-05-19 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_address_address_user_addres_title_6c7574_idx'),
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasties', '0007_rename_recepie_tasty_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by_user_id', related_query_name='%(app_label)s_%(class)s_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='order',
            name='modifier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated_by_user_id', related_query_name='%(app_label)s_%(class)s_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modifier'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='tasty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='tasties.tasty'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['reference'], name='orders_orde_referen_cf3026_idx'),
        ),
    ]
