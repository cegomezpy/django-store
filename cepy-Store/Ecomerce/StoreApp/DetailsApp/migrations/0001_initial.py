# Generated by Django 4.2 on 2023-06-29 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('StoreApp', '0010_delete_review'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('rating', models.PositiveIntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='Date the review was published')),
                ('date_edited', models.DateTimeField(help_text='Date the review was edited', null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreApp.product')),
            ],
        ),
    ]
