# Generated by Django 5.0.6 on 2024-07-09 13:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0017_scenario_beach_beach_lat_beach_beach_lon"),
    ]

    operations = [
        migrations.AddField(
            model_name="beach",
            name="beach_widget_id",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="beach",
            name="nx",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="beach",
            name="ny",
            field=models.IntegerField(null=True),
        ),
    ]
