#!/usr/bin/env python
"""
Script para actualizar las rutas de imágenes en la base de datos.
Ejecutar con: python fix_images.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Post
from portfolio.models import Project

def fix_blog_images():
    """Actualizar rutas de imágenes del blog."""
    print("🔧 Actualizando imágenes del blog...")
    
    # Mapeo de rutas viejas a nombres de archivo
    blog_mapping = {
        'blog/2025/11/Blog_Post_Rest_Api_Cover_jyIIfYW_tkKk4rO.png': 'Blog_Post_Rest_Api_Cover_jyIIfYW.png',
        'static/images/Qué_Bolá_Python_Episodio_1_Cover.png': 'Qué_Bolá_Python_Episodio_1_Cover.png',
        'static/images/Qué_Bolá_Python_Episodio_2_Cover.png': 'Qué_Bolá_Python_Episodio_2_Cover.png',
        'static/images/Qué_Bolá_Python_Episodio_3_Cover.png': 'Qué_Bolá_Python_Episodio_3_Cover.png',
    }
    
    posts = Post.objects.all()
    for post in posts:
        old_image = str(post.image)
        
        # Si ya es solo un nombre de archivo, skip
        if '/' not in old_image:
            print(f"  ✓ {post.name}: Ya está correcto ({old_image})")
            continue
            
        # Extraer solo el nombre del archivo
        filename = old_image.split('/')[-1]
        
        # Actualizar
        post.image = filename
        post.save()
        print(f"  ✓ {post.name}: {old_image} → {filename}")
    
    print(f"✅ {posts.count()} posts actualizados\n")

def fix_portfolio_images():
    """Actualizar rutas de imágenes del portfolio."""
    print("🔧 Actualizando imágenes del portfolio...")
    
    projects = Project.objects.all()
    for project in projects:
        old_image = str(project.image)
        
        # Si ya es solo un nombre de archivo, skip
        if '/' not in old_image:
            print(f"  ✓ {project.title}: Ya está correcto ({old_image})")
            continue
            
        # Extraer solo el nombre del archivo
        filename = old_image.split('/')[-1]
        
        # Actualizar
        project.image = filename
        project.save()
        print(f"  ✓ {project.title}: {old_image} → {filename}")
    
    print(f"✅ {projects.count()} proyectos actualizados\n")

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ARREGLANDO RUTAS DE IMÁGENES")
    print("=" * 60 + "\n")
    
    fix_blog_images()
    fix_portfolio_images()
    
    print("=" * 60)
    print("✅ ¡COMPLETADO!")
    print("=" * 60)
