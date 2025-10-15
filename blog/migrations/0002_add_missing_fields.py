# Generated manually to add missing fields to existing database

from django.db import migrations, models
from django.db import connection


def add_slug_if_not_exists(apps, schema_editor):
    """Add slug field to Category only if it doesn't exist"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='blog_category' AND column_name='slug'
        """)
        if not cursor.fetchone():
            # Column doesn't exist, add it
            cursor.execute("""
                ALTER TABLE blog_category 
                ADD COLUMN slug VARCHAR(20) NULL UNIQUE
            """)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        # Add slug field to Category (only if doesn't exist)
        migrations.RunPython(add_slug_if_not_exists, migrations.RunPython.noop),
        
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
