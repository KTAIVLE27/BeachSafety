# Generated by Django 5.0.6 on 2024-07-03 13:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0010_rename_board_id_event_board_event_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event_board",
            name="event_id",
            field=models.AutoField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="notice_board",
            name="notice_id",
            field=models.AutoField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
