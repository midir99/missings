# Generated by Django 4.0.4 on 2022-05-03 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("counters", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="missingpersonpost",
            name="alert_type",
            field=models.CharField(
                blank=True,
                choices=[("AL", "Alba"), ("AM", "Amber"), ("OD", "Odisea")],
                help_text="Please enter the alert or protocol type of this missing person post.",
                max_length=2,
                verbose_name="alert type",
            ),
        ),
    ]