# Generated by Django 4.2.3 on 2023-08-16 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("UserApp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="address",
            new_name="direccion",
        ),
        migrations.RenameField(
            model_name="client",
            old_name="mobile_number",
            new_name="numero_telefonico",
        ),
    ]