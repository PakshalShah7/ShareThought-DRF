# Generated by Django 4.2.1 on 2023-06-02 10:00

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_alter_user_managers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=128,
                null=True,
                region=None,
                unique=True,
                verbose_name="Phone Number",
            ),
        ),
    ]
