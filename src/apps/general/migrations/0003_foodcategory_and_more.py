# Generated by Django 4.2 on 2023-05-02 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='Modify time')),
                ('name', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by_user_id', related_query_name='%(app_label)s_%(class)s_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated_by_user_id', related_query_name='%(app_label)s_%(class)s_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddIndex(
            model_name='foodcategory',
            index=models.Index(fields=['name'], name='general_foo_name_9af758_idx'),
        ),
    ]