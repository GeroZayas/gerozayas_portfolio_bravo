# Generated manually to add missing fields to existing database

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        # Add slug field to Category
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=20, null=True, unique=True),
        ),
        
        # Alter Post slug to be unique
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, db_index=True),
        ),
        
        # Alter Post image path
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='blog/%Y/%m/'),
        ),
        
        # Add db_index to Post fields
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        
        # Add db_index to Comment
        migrations.AlterField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
