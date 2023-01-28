# Generated by Django 4.1.4 on 2023-01-12 13:21

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="title",
            new_name="name",
        ),
        migrations.AddField(
            model_name="post",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="body",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
