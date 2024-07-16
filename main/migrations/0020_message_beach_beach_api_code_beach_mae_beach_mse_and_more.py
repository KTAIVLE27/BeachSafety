# Generated by Django 5.0.6 on 2024-07-16 07:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0019_alter_event_board_beach_no_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("message_id", models.AutoField(primary_key=True, serialize=False)),
                ("message_code", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "message",
            },
        ),
        migrations.AddField(
            model_name="beach",
            name="beach_api_code",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="beach",
            name="mae",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="beach",
            name="mse",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="beach",
            name="r2score",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
